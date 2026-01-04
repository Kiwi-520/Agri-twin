from fastapi import FastAPI
from stable_baselines3 import PPO
import numpy as np

from backend.rl.agritwin_env import AgriTwinEnv
from backend.rl.fertilizer_advisory import fertilizer_advisory
from backend.rl.irrigation_explain import explain_irrigation

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


env = AgriTwinEnv()
model = PPO.load(
    "backend/models/ppo_agritwin_demo_v4",
    env = env
)

obs, _ = env.reset(seed = None)

@app.post("/reset")
def reset_simulation():
    global obs
    obs, _ = env.reset()

    return{
        "soil_moisture": float(obs[0]),
        "heat_stress": float(obs[1]),
        "rainfall": float(obs[2]),
        "crop_stage": float(obs[3]),
    }

@app.post("/step")
def step_simulation():
    global obs

    action, _= model.predict(obs, deterministic = True)

    obs, reward, terminated, truncated, info = env.step(action)

    fertilizer_info = fertilizer_advisory(
        soil_moisture=obs[0],
        heat_stress=obs[1],
        crop_stage=obs[3]
    )

    irrigation_reason = explain_irrigation(obs, action)

    return{
        "soil_moisture": float(obs[0]),
        "heat_stress": float(obs[1]),
        "rainfall": float(obs[2]),
        "crop_stage": float(obs[3]),
        "irrigation_mm": float(action[0]),
        "reward": float(reward),
        "fertilizer": fertilizer_info["fertilizer"],
        "fertilizer_reason": fertilizer_info["reason"],
        "irrigation_reason": irrigation_reason,
        "done": bool(terminated or truncated)
    }