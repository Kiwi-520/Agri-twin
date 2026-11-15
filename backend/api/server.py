from fastapi import FastAPI
from stable_baselines3 import PPO
import numpy as np
from dataclasses import feild, dataclass
import uuid
import os
from fastapi import HTTPException

from backend.rl.agritwin_env import AgriTwinEnv
from backend.rl.fertilizer_advisory import fertilizer_advisory
from backend.rl.irrigation_explain import explain_irrigation

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@dataclass
class Simsession:
    env : AgriTwinEnv
    obs : np.ndarray
    step_count : int = 0
    episode_log : list = feild(default_factory=list)

sessions = {}

# sid = str(uuid.uuid4())

@app.post("/rest")
def reset_simulation(session_id: str = None):
    sid = session_id or str(uuid.uuid4())

    env = AgriTwinEnv()
    obs, _ = env.rest()

    sessions[sid] = Simsession(
        env = env,
        obs = obs
    )

    return{
        "session_id":sid,
        **_obs_to_dict(obs)
    }

@app.post("/step")
def step_stimulation(session_id: str):
    try:
        if session_id not in sessions:
            raise HTTPException(
                status_code=404,
                detail="Session not found...."
            )
        session = sessions[session_id]
        action, _= model.predict(
            obs,
            deterministic = True
        )
        obs, reward, terminated, truncated, info = session.env.step(action)

        session.obs = obs
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

env = AgriTwinEnv()

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "../model/ppo_agritwin_demo_v4"
)
model = PPO.load(
    MODEL_PATH,
    env = env
)