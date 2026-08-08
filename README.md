# IoT Energy Optimization using Deep Reinforcement Learning

شبیه‌سازی شبکه حسگر IoT با باتری محدود و بهینه‌سازی تصمیم **ارسال / خواب** با عامل **DQN**.

پروژه شامل شبیه‌ساز، محیط Gymnasium، آموزش DQN، داشبورد Streamlit، ارزیابی سیاست‌ها، پیش‌نویس گزارش و پوستر است.

## Features

- IoT network simulation (Node, Packet, Gateway, Energy model)
- Distance-aware TX energy + simple packet-loss channel + AoI
- Baseline policies: Always Transmit / Always Sleep / Random
- Deep Q-Network with Stable-Baselines3
- Metrics and policy comparison charts
- Streamlit dashboard for run / train / compare
- Report draft + printable poster under `docs/`

## Technologies

- Python, Streamlit, Gymnasium, Stable-Baselines3
- NumPy, Pandas, Matplotlib, Altair, Jupyter

## Project structure

```text
IoT-Energy-Optimization-DRL/
├── app/
│   ├── ui/            # Streamlit dashboard
│   ├── simulation/    # Node, packet, gateway, simulator
│   ├── rl/            # Env, reward, DQN, trainer
│   ├── analytics/     # Metrics, evaluation, plots
│   └── config/        # Settings
├── notebooks/         # Step-by-step experiments
├── docs/
│   ├── report/        # Chapters 1-5 (Persian draft)
│   ├── poster/        # Poster content + HTML preview
│   ├── diagrams/
│   └── references/
├── experiments/       # Saved models (gitignored)
├── tests/
├── main.py
├── requirements.txt
└── README.md
```

## Setup

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
```

## Run dashboard

```bash
streamlit run main.py
```

Suggested UI flow:

1. Set nodes (≤ 10), steps, energy costs
2. Click **Train DQN**
3. Run with policy **DQN**
4. Click **Compare Policies**

## Smoke test

```bash
python tests/test_smoke.py
```

## Notebooks

| Notebook | Purpose |
|----------|---------|
| `01_node_simulation.ipynb` | Node + energy |
| `02_simulation_core.ipynb` | Simulator baselines |
| `03_packet_generation.ipynb` | Packet + gateway |
| `04_rl_environment_testing.ipynb` | Gym env |
| `05_dqn_training.ipynb` | DQN train |
| `06_results_analysis.ipynb` | Comparison plots |

## Docs

- Report chapters: `docs/report/`
- Poster text: `docs/poster/poster_content.md`
- Poster preview: open `docs/poster/poster.html` in a browser
- References: `docs/references/references.bib`

## License / status

Bachelor project — implementation and documentation drafts are ready for final university formatting.
