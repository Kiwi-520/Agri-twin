**Version:** v0.1 (Prototype)

# 🌾 Agri-Twin Backend

**Agri-Twin** is a **reinforcement-learning-driven digital twin for precision agriculture**, designed to optimize irrigation decisions and provide intelligent fertilizer recommendations. This backend powers the AI-driven farm simulation, enabling data-driven crop management.

---

## 📌 Overview

The backend is a **Python-based decision support system** that:

* Simulates crop growth under varying environmental conditions
* Uses a **Proximal Policy Optimization (PPO)** agent to optimize irrigation
* Provides fertilizer recommendations tailored to crop stage, soil, and stress
* Exposes a **REST API** to communicate with the frontend dashboard

**Key Goal:** Enable autonomous, efficient, and explainable irrigation decisions while ensuring crop health and water conservation.

---

## 🏗️ Architecture

### Core Components

| Component                                          | Purpose                                                                      |
| -------------------------------------------------- | ---------------------------------------------------------------------------- |
| **RL Environment (`agritwin_env.py`)**             | Simulates crop growth and environmental factors for agent training           |
| **Training Pipeline (`train_ppo.py`)**             | Trains PPO agent on the custom environment                                   |
| **Agent Execution (`run_agent.py`)**               | Runs trained agent, logs actions, and visualizes results                     |
| **Fertilizer Advisory (`fertilizer_advisory.py`)** | Recommends fertilizer based on crop growth stage, soil moisture, and stress  |
| **REST API Server (`server.py`)**                  | Provides endpoints for frontend to interact with the simulation in real-time |

---

## 📂 Directory Structure

```
backend/
├── api/
│   └── server.py                  # FastAPI server for frontend
├── models/
│   └── ppo_agritwin_demo_v4.zip   # Trained PPO model
├── rl/
│   ├── __init__.py
│   ├── agritwin_env.py            # Custom Gymnasium RL environment
│   ├── train_ppo.py               # PPO model training
│   ├── run_agent.py               # Agent simulation and visualization
│   ├── fertilizer_advisory.py     # Fertilizer recommendation logic
│   ├── test_env.py                # Environment test scripts
│   └── wofost_env.py              # Optional WOFOST crop model wrapper
└── requirements.txt               # Python dependencies
```

---

## ⚙️ Core Files Explained

### 1. **`agritwin_env.py`** – RL Environment

**Purpose:** Simulates the farm environment for RL agent training.

**Observation Space (4 values):**

| Feature         | Range   | Description                                    |
| --------------- | ------- | ---------------------------------------------- |
| `soil_moisture` | [0,1]   | Current soil water content                     |
| `heat_stress`   | [0,1]   | Crop temperature stress                        |
| `rainfall`      | [0,0.1] | Daily rainfall                                 |
| `crop_stage`    | [0,1]   | Crop development stage (0=seedling, 1=harvest) |

**Action Space:**

* Continuous: `irrigation_amount` in mm/day [0–50]

**Reward Function:**

* Positive for maintaining optimal soil moisture (0.4–0.7)
* Negative for over/under-watering
* Penalty for irrigation cost inefficiency

**Step Logic:**

1. Apply irrigation action
2. Update soil moisture (evaporation, rainfall, drainage)
3. Apply heat stress effects
4. Advance crop growth stage
5. Calculate reward
6. Return new observation

---

### 2. **`train_ppo.py`** – Model Training

**Purpose:** Trains the PPO agent on the Agri-Twin environment.

**Training Flow:**

1. Initialize environment
2. Define PPO agent with MLP policy network
3. Train agent over defined timesteps (~100,000)
4. Save trained model to `models/`

**Output:**

* Trained model: `ppo_agritwin_demo_v4.zip`
* Training metrics and logs for evaluation

---

### 3. **`run_agent.py`** – Agent Execution & Visualization

**Purpose:** Executes the trained agent to simulate irrigation decisions and visualize results.

**Workflow:**

1. Reset environment
2. Load trained PPO model
3. Loop until episode ends:
   * Observe current state
   * Predict irrigation action
   * Apply action in environment
   * Receive new observation and reward
   * Log actions and environmental variables
   * Generate fertilizer recommendation
   * Optionally explain action rationale

**Visualization Outputs:**

* Soil moisture trends
* Irrigation timeline
* Reward accumulation
* Crop growth curve
* Heat stress evolution

**Explainable Decisions Example:**

> "Low soil moisture detected + crop in vegetative stage → irrigate 15mm"

---

### 4. **`fertilizer_advisory.py`** – Fertilizer Recommendation

**Function:** `fertilizer_advisory(soil_moisture, heat_stress, crop_stage) → dict`

**Logic:**

* Early stage: High nitrogen
* Mid-stage: Balanced NPK
* Flowering: Phosphorus + Potassium
* Maturity: Minimal application

**Stress Adjustments:**

* Heat stress → Add micronutrients
* Low moisture → Fertilizer effectiveness warning

**Output Example:**

```json
{
  "fertilizer": "Balanced NPK",
  "reason": "Mid-stage growth + heat stress detected"
}
```

---

### 5. **`server.py`** – FastAPI REST API

**Purpose:** Exposes backend functionalities to the frontend.

**Endpoints:**

| Endpoint | Method | Description                              |
| -------- | ------ | ---------------------------------------- |
| `/reset` | POST   | Reset simulation to initial state        |
| `/step`  | POST   | Execute one timestep with agent decision |

**`/reset` Response Example:**

```json
{
  "soil_moisture": 0.45,
  "heat_stress": 0.12,
  "rainfall": 0.02,
  "crop_stage": 0.0
}
```

**`/step` Response Example:**

```json
{
  "soil_moisture": 0.52,
  "heat_stress": 0.18,
  "rainfall": 0.01,
  "crop_stage": 0.15,
  "irrigation_mm": 12.5,
  "reward": 0.82,
  "fertilizer": "High Nitrogen",
  "fertilizer_reason": "Early growth stage needs nitrogen",
  "done": false
}
```

---

## 🔄 Backend Workflow

### Training Phase (One-time)

```
1. Create environment
2. Initialize PPO agent
3. Agent explores actions
4. Environment provides rewards
5. Agent updates policy
6. Repeat until convergence
7. Save trained model
```

### Inference Phase (Runtime)

```
Frontend → FastAPI Server
           ↓
  Load trained PPO model
           ↓
  Get current environment state
           ↓
  Model predicts irrigation
           ↓
  Apply irrigation → update environment
           ↓
  Fertilizer recommendation
           ↓
  Return results to frontend
```

---

## 🧰 Dependencies

### Core

* `stable-baselines3` (PPO agent)
* `gymnasium` (custom environment interface)
* `numpy`, `torch` (numerical & neural networks)

### API

* `fastapi`, `uvicorn` (server)
* `python-dotenv` (config)

### Visualization

* `matplotlib`, `seaborn`

### Optional

* `pcse` (WOFOST crop model integration)

---

## ⚙️ Setup Instructions

```bash
# 1. Create virtual environment
python -m venv env_agritwin
# Windows
env_agritwin\Scripts\activate
# Linux/Mac
source env_agritwin/bin/activate

# 2. Install dependencies
cd backend
pip install -r requirements.txt

# 3. Train model (optional)
python rl/train_ppo.py

# 4. Test agent locally
python rl/run_agent.py

# 5. Start API server
uvicorn backend.api.server:app --reload --port 5000
```

Server URL: `http://127.0.0.1:5000`

---

## 🔍 Model Details

* **Algorithm:** Proximal Policy Optimization (PPO)
* **Network:** MLP (2–3 hidden layers)
* **Input:** 4 observation features
* **Output:** Continuous irrigation action [0–50mm]
* **Training Steps:** ~100,000
* **Objective:** Maximize crop health & water efficiency

---

## 🛠️ Troubleshooting

| Issue              | Solution                                                  |
| ------------------ | --------------------------------------------------------- |
| ImportError: `gym` | Install `gymnasium` and update imports                    |
| Model not found    | Verify path: `backend/models/ppo_agritwin_demo_v4.zip`    |
| CORS errors        | Check `allow_origins` in FastAPI                          |
| Server won't start | Ensure port 5000 is free: `netstat -ano \| findstr :5000` |

---

## 🚀 Future Enhancements

1. Multi-crop support
2. Integration with real weather APIs
3. WOFOST scientific crop modeling
4. Historical data learning
5. Multi-agent coordination
6. Enhanced explainable AI
7. Database storage for simulations
8. Real-time IoT monitoring

---

## 📝 Authors

* Team: Byte

---