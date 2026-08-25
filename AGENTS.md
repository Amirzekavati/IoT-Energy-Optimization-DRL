# AGENTS.md

## Cursor Cloud specific instructions

This is a single Python 3.12 project: an IoT sensor-network energy optimizer that
trains a DQN (Stable-Baselines3 / PyTorch) and exposes a Streamlit dashboard.
There is no database, no Docker, and no separate backend service — the simulator,
RL trainer, and analytics are in-process libraries used by the UI, tests, and notebooks.

### Environment / dependencies

- Dependencies are installed into a project-local virtualenv at `venv/` (gitignored).
  The startup update script recreates/refreshes it via `python3 -m venv venv` +
  `venv/bin/pip install -r requirements.txt`, so it is available on boot.
- Always run project commands with the venv active (`source venv/bin/activate`) or
  via `venv/bin/python` / `venv/bin/streamlit`.
- The install pulls PyTorch plus NVIDIA CUDA wheels (large, ~1GB+). CPU-only is fine
  for development; no GPU is required.

### Run / test / build (see `README.md` for the canonical list)

- Tests: `python tests/test_smoke.py` — the only test suite (stdlib `unittest`,
  not pytest). Fast (~1-4s); trains a tiny DQN end-to-end.
- Dev server (dashboard): `streamlit run main.py` (default port 8501). In a
  headless VM use `streamlit run main.py --server.headless true --server.port 8501`.
- Lint: none configured (no ruff/flake8/black/pyproject.toml). There is no build step.

### Non-obvious notes

- Trained DQN models are written to `experiments/models/` (gitignored); the dir is
  created at runtime.
- Streamlit UI flow: Train DQN → select policy "DQN" → Run Simulation → Compare
  Policies. "Compare Policies" only includes DQN when a trained agent exists in the
  current session state; otherwise it compares baselines only.
