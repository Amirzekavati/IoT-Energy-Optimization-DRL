# IoT Energy Optimization using Deep Reinforcement Learning

This project focuses on optimizing energy consumption in IoT networks using Deep Reinforcement Learning (DRL).

A simulation environment is designed consisting of IoT sensor nodes with limited battery energy. The system generates synthetic sensor data and uses a DRL agent to decide whether nodes should transmit data or switch to sleep mode in order to reduce energy consumption and increase network lifetime.

The project includes:
- IoT network simulation
- Energy consumption modeling
- Packet generation and scheduling
- Deep Reinforcement Learning (DQN)
- Streamlit-based visualization dashboard
- Metrics analysis and evaluation

## Technologies

- Python
- Streamlit
- Gymnasium
- Stable-Baselines3
- NumPy
- Pandas
- Matplotlib
- Jupyter Notebook

## Structure

```text
Iot-Energy-Optimization-DRL/
│
├── app/
│   ├── ui/
│   │   ├── dashboard.py
│   │   ├── controls.py
│   │   ├── charts.py
│   │   └── node_manager.py
│   │
│   ├── simulation/
│   │   ├── node.py
│   │   ├── gateway.py
│   │   ├── packet.py
│   │   ├── energy_model.py
│   │   ├── simulator.py
│   │   └── scheduler.py
│   │
│   ├── rl/
│   │   ├── environment.py
│   │   ├── reward.py
│   │   ├── dqn_agent.py
│   │   └── trainer.py
│   │
│   ├── analytics/
│   │   ├── metrics.py
│   │   ├── evaluator.py
│   │   └── plots.py
│   │
│   ├── config/
│   │   └── settings.py
│   │
│   └── main.py
│
├── experiments/
│
├── docs/
│   ├── report/
│   ├── poster/
│   ├── diagrams/
│   └── references/
│
├── tests/
│
├── requirements.txt
├── README.md
└── .gitignore

## Run Project

```bash
pip install -r requirements.txt
streamlit run main.py

---

Project is currently under development.