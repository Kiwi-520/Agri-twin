import gymnasium as gym
from gymnasium import spaces
import numpy as np

class AgriTwinEnv(gym.Env):
    """
    Custom Gym Environment for Agri-Twin:
     Autonomous irrigation control using Reinforcement Learning.
    """
    # Max daily irrigation in mm/day
    MAX_IRRIGATION_MM = 50.0

    def __init__(self):
        super().__init__()

        """
        ACTION SPACE
        Action = irrigation amount in mm/day
        Continuous control problem
        """
        self.action_space = spaces.Box(
            low = 0.0,
            high = self.MAX_IRRIGATION_MM,
            shape = (1,),
            dtype = np.float32

        )

        """
        OBSERVATION SPACE
        [soil_moisture, heat_stress, rainfall, crop_stage]
        State vector (all normalized to [0, 1]):
        """
        self.observation_space = spaces.Box(
            low = 0.0,
            high = 1.0,
            shape = (4,),
            dtype = np.float32
        )

        self.max_steps = 60
        self.current_step = 0

        # Internal (real-world) state
        self.reset(seed = None)

    

    def reset(self, *, seed=None, options = None):
        super().reset(seed = seed)
        self.current_step = 0
        
         # Internal (real-world) state
        self.soil_moisture = np.random.uniform(0.3, 0.45)
        self.heat_stress = np.random.uniform(0.0, 0.05)
        self.rainfall = 0.0
        self.crop_stage = 0.1

        observation = np.array([
            self.soil_moisture,
            self.heat_stress,
            self.rainfall,
            self.crop_stage 
        ], dtype = np.float32)


        return observation, {}



    def step(self, action):

        self.current_step += 1
        # Convert normalized action to irrigation in mm
        if isinstance(action, (np.ndarray, list)):
            irrigation_mm = float(action[0])
        else:
            irrigation_mm = float(action)
            
        # self.rainfall = np.random.uniform(0.0, 0.2)
        if np.random.rand() < 0.1:
            self.rainfall = np.random.uniform(0.01, 0.03)
        else:
            self.rainfall = 0.0

        # Simple water balance
        evap_loss = 0.03 + 0.07 * self.heat_stress
        irrigation_normalized = irrigation_mm / self.MAX_IRRIGATION_MM 
        self.soil_moisture += irrigation_normalized + self.rainfall - evap_loss
        # Clamp soil moisture betweeen [0,1]
        self.soil_moisture = np.clip(self.soil_moisture, 0.0, 1.0)

        # Heat stress dynamics
        # v2
        # if self.soil_moisture < 0.3:
        #     self.heat_stress += 0.1
        # elif self.soil_moisture > 0.7:
        #     self.heat_stress -= 0.05
        # else:
        #     self.heat_stress -= 0.05

        # v3
        # if self.soil_moisture < 0.35:
        #     self.heat_stress += 0.08
        # else:
        #     self.heat_stress -= 0.03

        # v4
        # Heat stress dynamics v4 (demo-friendly)
        if self.soil_moisture < 0.4:               # low soil → heat stress rises faster
            self.heat_stress += 0.05
        elif self.soil_moisture > 0.7:             # high soil → heat stress decreases faster
            self.heat_stress -= 0.03
        else:                                       # moderate soil → slight recovery
            self.heat_stress += 0.01 - 0.02 * np.random.rand()  # small random fluctuation
        self.heat_stress = np.clip(self.heat_stress, 0.0, 1.0)

        #  Clamp heat stress between [0,1]
        self.heat_stress = np.clip(self.heat_stress, 0.0, 1.0)

        # Crop stage
        # if self.soil_moisture < 0.25:
        #     growth_rate = 0.0
        # else:
        #     growth_rate = 0.02 * (1.0 - self.heat_stress)
        growth_rate = 0.01 * (1.0 - self.heat_stress)
            
        self.crop_stage += growth_rate
        self.crop_stage = np.clip(self.crop_stage, 0.0, 1.0)

        # Reward Shaping 

        # growth reward
        reward_growth = growth_rate * 50.0
        # heat stress reward
        reward_stress = - self.heat_stress * 5.0
        # water reward 
        reward_water = - (irrigation_mm/ self.MAX_IRRIGATION_MM) * 0.3
        reward_soil = -abs(self.soil_moisture - 0.5) * 0.5
        # total reward
        reward = reward_growth + reward_stress + reward_water + reward_soil
        if self.soil_moisture < 0.4:
            reward += 0.2
  

        # Terminated
        terminated = self.crop_stage >= 1.0
        truncated = self.current_step >= self.max_steps

        observation = np.array([
            self.soil_moisture,
            self.heat_stress,
            self.rainfall,
            self.crop_stage 
        ], dtype = np.float32)

        info = {
            "soil moisture": self.soil_moisture,
            "heat stress": self.heat_stress,
            "rainfall": self.rainfall,
            "crop stage": self.crop_stage,
            "irrigation": irrigation_mm,
        }

        return observation, reward, terminated, truncated, info
    
    