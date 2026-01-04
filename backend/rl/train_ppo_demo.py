from agritwin_env import AgriTwinEnv
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3 import PPO
import numpy as np
import os

# env = make_vec_env(AgriTwinEnv, n_envs = 1)
# state = env.reset()
# print("Initial state: ", state)

# random_action = env.action_space.sample()
# next_state, reward, done, info = env.step(random_action)
# print("Next state: ", next_state)
# print("Reward: ", reward)
env = AgriTwinEnv()

model = PPO(
    policy = "MlpPolicy",
    env = env,
    verbose = 1,
    learning_rate = 3e-4,
    gamma = 0.98,
    n_steps = 1024,
    batch_size = 256

)

model.learn(total_timesteps = 200_000)
save_path = os.path.join(os.path.dirname(__file__), "../models/ppo_agritwin_demo")
model.save(save_path)
print(f"PPO model saved successfully at {save_path}.zip!")
print(model.policy)