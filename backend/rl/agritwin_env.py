import gymnasium as gym
from gymnasium import spaces
import numpy as np


def get_kc(crop_stage: float) -> float:
    """
    FAO-56 crop coefficient (Kc) by normalized growth stage.
    Source: Allen et al. (1998), FAO Irrigation and Drainage Paper 56, Table 12.
    Generic cereal crop (wheat/rice proxy).
    """
    if crop_stage < 0.20:
        return 0.40
    elif crop_stage < 0.45:
        t = (crop_stage - 0.20) / 0.25
        return 0.40 + t * 0.75
    elif crop_stage < 0.75:
        return 1.15
    else:
        t = (crop_stage - 0.75) / 0.25
        return 1.15 - t * 0.80


class AgriTwinEnv(gym.Env):
    """
    Agri-Twin RL Environment v2.

    Simulates daily irrigation decision-making for a single crop field.
    Physics grounded via FAO-56 ET model (Allen et al. 1998).
    Observation space includes electricity availability window —
    a real constraint in smallholder farming across India.

    Observation (7 variables):
        [soil_moisture, heat_stress, last_rain, rain_forecast,
         crop_stage, power_available, hour_normalized]

    Action:
        irrigation_mm in [0, MAX_IRRIGATION_MM]
    """

    MAX_IRRIGATION_MM = 30.0   # realistic daily max for smallholder drip/sprinkler
    BASE_ETO = 0.05            # reference evapotranspiration (calibratable per region)
    FIELD_CAPACITY = 0.80      # soil moisture above this drains

    def __init__(self):
        super().__init__()

        self.action_space = spaces.Box(
            low=0.0,
            high=self.MAX_IRRIGATION_MM,
            shape=(1,),
            dtype=np.float32
        )

        self.observation_space = spaces.Box(
            low=np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=np.float32),
            high=np.array([1.0, 1.0, 0.05, 0.05, 1.0, 1.0, 1.0], dtype=np.float32),
            dtype=np.float32
        )

        self.max_steps = 80
        self.current_step = 0
        # Do NOT call reset() here — let SB3 handle seeding properly

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        self.current_step = 0

        # Initial conditions — realistic for wheat sowing (Rabi season, India)
        self.soil_moisture = np.random.uniform(0.35, 0.50)
        self.heat_stress = np.random.uniform(0.0, 0.03)
        self.last_rain = 0.0
        self.rain_forecast = 0.0
        self.crop_stage = 0.10

        # Electricity window (varies day to day — forces agent to generalize)
        self.current_hour = np.random.randint(0, 24)
        self.power_window_start = int(np.random.choice([1, 6, 14, 20]))
        self.power_window_hours = 6

        return self._get_obs(), {}

    def _get_obs(self):
        power_available = 1.0 if (
            self.current_hour >= self.power_window_start and
            self.current_hour < self.power_window_start + self.power_window_hours
        ) else 0.0

        return np.array([
            self.soil_moisture,
            self.heat_stress,
            self.last_rain,
            self.rain_forecast,
            self.crop_stage,
            power_available,
            self.current_hour / 24.0
        ], dtype=np.float32)

    def step(self, action):
        self.current_step += 1

        irrigation_mm = float(action[0]) if isinstance(action, (np.ndarray, list)) else float(action)
        irrigation_mm = np.clip(irrigation_mm, 0.0, self.MAX_IRRIGATION_MM)

        # --- RAIN ---
        # Forecast from last step becomes actual rain this step
        self.last_rain = self.rain_forecast
        # Sample NEXT step's forecast (agent acts on this, not last_rain)
        self.rain_forecast = float(np.random.uniform(0.01, 0.03)) if np.random.rand() < 0.1 else 0.0

        # --- WATER BALANCE ---
        kc = get_kc(self.crop_stage)
        evap_loss = self.BASE_ETO * kc * (1.0 + 0.5 * self.heat_stress)
        irrigation_normalized = irrigation_mm / self.MAX_IRRIGATION_MM
        self.soil_moisture += irrigation_normalized + self.last_rain - evap_loss

        # Drainage above field capacity
        if self.soil_moisture > self.FIELD_CAPACITY:
            drainage = (self.soil_moisture - self.FIELD_CAPACITY) * 0.40
            self.soil_moisture -= drainage

        self.soil_moisture = np.clip(self.soil_moisture, 0.0, 1.0)

        # --- HEAT STRESS ---
        if self.soil_moisture < 0.40:
            self.heat_stress += 0.05
        elif self.soil_moisture > 0.70:
            self.heat_stress -= 0.03
        else:
            self.heat_stress += 0.01 - 0.02 * np.random.rand()
        self.heat_stress = np.clip(self.heat_stress, 0.0, 1.0)

        # --- CROP GROWTH (FAO Kc-modulated) ---
        growth_rate = 0.015 * (1.0 - self.heat_stress)
        # Growth pauses if severely dry
        if self.soil_moisture < 0.25:
            growth_rate *= 0.10
        self.crop_stage = np.clip(self.crop_stage + growth_rate, 0.0, 1.0)

        # --- ELECTRICITY ---
        power_available = 1.0 if (
            self.current_hour >= self.power_window_start and
            self.current_hour < self.power_window_start + self.power_window_hours
        ) else 0.0
        self.current_hour = (self.current_hour + 1) % 24

        # --- REWARD ---
        reward_growth = growth_rate * 50.0                             # crop progress
        reward_stress = -self.heat_stress * 5.0                        # penalize stress
        reward_water = -(irrigation_mm / self.MAX_IRRIGATION_MM) * 0.3 # penalize waste
        reward_soil = -abs(self.soil_moisture - 0.55) * 0.5            # target 0.55 (slightly above wilting point)
        reward_power = -irrigation_mm * 0.02 if (irrigation_mm > 0 and power_available < 0.5) else 0.0

        reward = reward_growth + reward_stress + reward_water + reward_soil + reward_power

        terminated = bool(self.crop_stage >= 1.0)
        truncated = bool(self.current_step >= self.max_steps)

        info = {
            "soil_moisture": self.soil_moisture,
            "heat_stress": self.heat_stress,
            "last_rain": self.last_rain,
            "rain_forecast": self.rain_forecast,
            "crop_stage": self.crop_stage,
            "irrigation_mm": irrigation_mm,
            "power_available": power_available,
            "kc": kc,
            "evap_loss": evap_loss,
            "reward_breakdown": {
                "growth": reward_growth,
                "stress": reward_stress,
                "water": reward_water,
                "soil": reward_soil,
                "power": reward_power
            }
        }

        return self._get_obs(), reward, terminated, truncated, info