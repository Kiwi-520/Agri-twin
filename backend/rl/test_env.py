from agritwin_env import AgriTwinEnv

env = AgriTwinEnv()
obs = env.reset()

for _ in range(10):
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)
    print(info)
