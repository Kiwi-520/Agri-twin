from stable_baselines3 import PPO
from agritwin_env import AgriTwinEnv
import numpy as np
import os
import matplotlib.pyplot as plt

env = AgriTwinEnv()

model_path = "C:/Users/disha/Disha/Projects/Agri-twin/Agri-twin/backend/models/ppo_agritwin.zip"
model = PPO.load(model_path, env = env)

obs, info = env.reset()
done = False
step = 0
total_reward = 0.0

# Loggin containers
timesteps = []
soil_moisture_log = []
heat_stress_log = []
irrigation_log = []
crop_stage_log = []
reward_log = []


while not done:
    action, _ = model.predict(obs, deterministic = True)
    obs, reward, terminated, truncated, info = env.step(action)
    # logging data
    timesteps.append(step)
    soil_moisture_log.append(obs[0])
    crop_stage_log.append(obs[1])
    heat_stress_log.append(obs[2])
    irrigation_log.append(action[0])
    reward_log.append(reward)

    done = terminated or truncated
    total_reward += reward


    print(
        f"Step {step:02d} |",
        f"Irrigation {action[0]:.2f} mm |"
        f"Reward {reward:.3f} |"
        f"Soil: {obs[0]:.2f} |"
        f"Crop: {obs[1]:.2f} |"
        f"Heat: {obs[2]:.2f} |"
    )

    step += 1

print("\n Episode finished")
print(f"Total steps: {step}")
print(f"Total reward: {total_reward:.3f}")

print("\n Log data summary ")
print(
    f"Steps: {len(timesteps)}\n"
    f"Soil moisture samples: {len(soil_moisture_log)}\n"
    f"Crop stage samples: {len(crop_stage_log)}\n"
    f"Heat stress samples: {len(heat_stress_log)}\n"
    f"Irriagtion samples: {len(irrigation_log)}\n"
    f"Reward samples: {len(reward_log)}\n"
)

plt.figure()
plt.plot(timesteps, soil_moisture_log)
plt.xlabel("Timesteps")
plt.ylabel("Soil Moisture")
plt.title("Soil Moisture Evolution")
plt.show()

plt.figure()
plt.plot(timesteps, irrigation_log)
plt.xlabel("Timesteps")
plt.ylabel("Irrigation (mm)")
plt.title("Irrigation Decisions overtime")
plt.show()

plt.figure()
plt.plot(timesteps, reward_log)
plt.xlabel("Timesteps")
plt.ylabel("Reward")
plt.title("Reward Over Time")
plt.show()

plt.figure()
plt.plot(timesteps, crop_stage_log)
plt.xlabel("Timesteps")
plt.ylabel("Crop Stage")
plt.title("Crop Stage Over Time")
plt.show()

plt.figure()
plt.plot(timesteps, heat_stress_log)
plt.xlabel("Timesteps")
plt.ylabel("Heat Stress")
plt.title("Heat Stress Over Time")
plt.show()