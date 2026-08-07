"""
Sidebar controls for the Streamlit dashboard.
"""

import streamlit as st

from app.config.settings import Settings


def render_controls():
    """
    Draw sidebar widgets and return a control dict.

    Keys:
      settings, policy_name, train_timesteps,
      run_clicked, train_clicked, compare_clicked
    """
    st.sidebar.header("Simulation Controls")

    defaults = Settings()

    num_nodes = st.sidebar.slider(
        "Number of nodes",
        min_value=1,
        max_value=10,
        value=min(defaults.NUM_NODES, 10),
        help="Max 10 so the action space stays DQN-friendly (Discrete 2^n).",
    )
    max_steps = st.sidebar.slider(
        "Max steps",
        min_value=10,
        max_value=500,
        value=defaults.MAX_STEPS,
        step=10,
    )
    initial_energy = st.sidebar.number_input(
        "Initial energy (J)",
        min_value=0.1,
        max_value=10.0,
        value=float(defaults.INITIAL_ENERGY),
        step=0.1,
    )
    seed = st.sidebar.number_input(
        "Random seed",
        min_value=0,
        max_value=10_000,
        value=int(defaults.RANDOM_SEED),
        step=1,
    )

    st.sidebar.subheader("Energy costs")
    tx_energy = st.sidebar.number_input(
        "Transmit cost",
        min_value=0.001,
        max_value=1.0,
        value=float(defaults.TX_ENERGY),
        step=0.001,
        format="%.3f",
    )
    sense_energy = st.sidebar.number_input(
        "Sense cost",
        min_value=0.001,
        max_value=1.0,
        value=float(defaults.SENSE_ENERGY),
        step=0.001,
        format="%.3f",
    )
    sleep_energy = st.sidebar.number_input(
        "Sleep cost",
        min_value=0.0001,
        max_value=1.0,
        value=float(defaults.SLEEP_ENERGY),
        step=0.0001,
        format="%.4f",
    )

    st.sidebar.subheader("Policy")
    policy_label = st.sidebar.selectbox(
        "Run policy",
        options=[
            "Always Transmit",
            "Always Sleep",
            "Random",
            "DQN",
        ],
        index=0,
    )
    policy_map = {
        "Always Transmit": "always_transmit",
        "Always Sleep": "always_sleep",
        "Random": "random",
        "DQN": "dqn",
    }
    policy_name = policy_map[policy_label]

    st.sidebar.subheader("DQN training")
    train_timesteps = st.sidebar.slider(
        "Train timesteps",
        min_value=500,
        max_value=20_000,
        value=min(defaults.TRAIN_TIMESTEPS, 3000),
        step=500,
    )

    run_clicked = st.sidebar.button("Run Simulation", type="primary")
    train_clicked = st.sidebar.button("Train DQN")
    compare_clicked = st.sidebar.button("Compare Policies")

    settings = Settings()
    settings.NUM_NODES = int(num_nodes)
    settings.MAX_STEPS = int(max_steps)
    settings.INITIAL_ENERGY = float(initial_energy)
    settings.RANDOM_SEED = int(seed)
    settings.TX_ENERGY = float(tx_energy)
    settings.SENSE_ENERGY = float(sense_energy)
    settings.SLEEP_ENERGY = float(sleep_energy)
    settings.TRAIN_TIMESTEPS = int(train_timesteps)

    return {
        "settings": settings,
        "policy_name": policy_name,
        "train_timesteps": int(train_timesteps),
        "run_clicked": run_clicked,
        "train_clicked": train_clicked,
        "compare_clicked": compare_clicked,
    }
