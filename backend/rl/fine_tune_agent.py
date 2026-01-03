from agritwin_env import AgriTwinEnv
from stable_baselines3 import PPO
import os

env = AgriTwinEnv()

model_path = os.path.join(os.path.dirname(__file__), "../models/ppo_agritwin_demo.zip")
model = PPO.load(model_path)
model.set_env(env)

model.learn(total_timesteps = 50_000)
save_path = os.path.join(os.path.dirname(__file__), "../models/ppo_agritwin_demo_v2")
model.save(save_path)
print(f"PPO model saved successfully at {save_path}.zip!")
