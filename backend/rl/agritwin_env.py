import gym
from gym import spaces
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

        # Internal (real-world) state
        self.reset()
    

    def reset(self, seed=None, options = None):
        super().reset(seed = seed)
        
         # Internal (real-world) state
        self.soil_moisture = 0.5
        self.heat_stress = 0.0
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
        # Convert normalized action to irrigation in mm
        irrigation_mm = float(action[0])
        self.rainfall = np.random.uniform(0.0, 0.2)

        # Simple water balance
        irrigation_normalized = irrigation_mm / self.MAX_IRRIGATION_MM 
        self.soil_moisture += irrigation_normalized + self.rainfall
        # Clamp soil moisture betweeen [0,1]
        self.soil_moisture = np.clip(self.soil_moisture, 0.0, 1.0)

        # Heat stress dynamics
        if self.soil_moisture < 0.3:
            self.heat_stress += 0.05
        else:
            self.heat_stress -= 0.03
        #  Clamp heat stress between [0,1]
        self.heat_stress = np.clip(self.heat_stress, 0.0, 1.0)

        # Crop stage
        growth_rate = 0.02 * (1.0 - self.heat_stress)
        self.crop_stage += growth_rate
        self.crop_stage = np.clip(self.crop_stage, 0.0, 1.0)

        # Reward
        # growth reward
        reward_growth = growth_rate * 10.0
        # heat stress reward
        reward_stress = - self.heat_stress * 5.0
        # water reward 
        reward_water = - (irrigation_mm/ self.MAX_IRRIGATION_MM) * 2
        # total reward
        reward = reward_growth + reward_stress + reward_water

        # Terminated
        terminated = self.crop_stage >= 1.0
        truncated = False

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

        
