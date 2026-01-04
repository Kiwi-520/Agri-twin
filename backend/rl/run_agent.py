from stable_baselines3 import PPO
from agritwin_env import AgriTwinEnv
import numpy as np
import os
import matplotlib.pyplot as plt
from fertilizer_advisory import fertilizer_advisory

def explain_action(obs, action):
    soil, heat, rain, crop = obs
    reasons = []

    # Adjust thresholds to match actual obs ranges
    if soil < 0.5:
        reasons.append("Soil low → irrigate more")
    if heat > 0.3:
        reasons.append("Heat stress high → irrigate to cool")
    if rain > 0.05:
        reasons.append("Rain predicted → irrigate less")
    if crop > 0.6:
        reasons.append("Crop nearing maturity → moderate irrigation")

    if not reasons:
        reasons.append("Conditions normal → small irrigation")

    explanation = " + ".join(reasons) 
    return f"Action: {action[0]:.2f} mm | Rationale: {explanation}"


env = AgriTwinEnv()

model_path = "C:/Users/disha/Disha/Projects/Agri-twin/Agri-twin/backend/models/ppo_agritwin_demo_v4.zip"
model = PPO.load(model_path, env = env)

obs, info = env.reset()
done = False
step = 0
total_reward = 0.0

# Loggin containers
timesteps = []
soil_moisture_log = []
heat_stress_log = []
rainfall_log = []
crop_stage_log = []
irrigation_log = []
reward_log = []
fertilizer_log = []


while not done:
    action, _ = model.predict(obs, deterministic = True)
    obs, reward, terminated, truncated, info = env.step(action)
    done = terminated or truncated
    #
    # Fertilization advisory
    fertilizer_info = fertilizer_advisory(
    soil_moisture=obs[0],
    heat_stress=obs[1],
    crop_stage=obs[3]
    )


    # Explanation fornirrirgation decision
    irrigation_explanation = explain_action(obs, action)

    # logging data
    timesteps.append(step)
    soil_moisture_log.append(obs[0])
    heat_stress_log.append(obs[1])
    rainfall_log.append(obs[2])
    crop_stage_log.append(obs[3])
    irrigation_log.append(action[0])
    reward_log.append(reward)
    fertilizer_log.append(fertilizer_info["fertilizer"])

    total_reward += reward

    print(
        f"\nStep {step:02d} | "
        f"Irrigation Rationale: {irrigation_explanation} | "
        f"Fertilizer: {fertilizer_info['fertilizer']} | "
        f"Fertilizer Reason: {fertilizer_info['reason']} | "
        f"Reward: {reward:.3f} | "
        f"Soil: {obs[0]:.2f} | "
        f"Heat: {obs[1]:.2f} | "
        f"Rain: {obs[2]:.2f} | "
        f"Crop Stage: {obs[3]:.2f}"
    )

    step += 1

print("\n Episode finished")
print(f"Total steps: {step}")
print(f"Total reward: {total_reward:.3f}")

print("\n Log data summary ")
print(
    f"Steps: {len(timesteps)}\n"
    f"Soil moisture samples: {len(soil_moisture_log)}\n"
    f"Heat stress samples: {len(heat_stress_log)}\n"
    f"Rainfall samples: {len(rainfall_log)}\n"
    f"Crop stage samples: {len(crop_stage_log)}\n"
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