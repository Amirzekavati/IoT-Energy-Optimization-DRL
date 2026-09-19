"""
Main Streamlit dashboard page.
"""

from pathlib import Path

from app.analytics.tensorboard_reader import (
    load_tensorboard_loss
)
import pandas as pd
import streamlit as st

from app.analytics import compare_policies, run_env_policy, run_simulator_policy
from app.rl import DQNAgent, train_dqn
from app.simulation import AlwaysSleepScheduler, Scheduler
from app.ui.charts import (
    render_comparison,
    render_dqn_loss,
    render_history_charts,
    render_summary_metrics,
    render_training_reward,
    render_reward_components,
    render_average_reward
)
from app.ui.controls import render_controls
from app.ui.node_manager import render_network_map, render_node_table


def _run_baseline(settings, policy_name):
    if policy_name == "always_sleep":
        return run_simulator_policy(
            settings, AlwaysSleepScheduler(), settings.RANDOM_SEED
        )
    return run_simulator_policy(settings, Scheduler(), settings.RANDOM_SEED)


def _run_random(settings):
    return run_env_policy(
        settings,
        action_fn=lambda env, obs: env.action_space.sample(),
        seed=settings.RANDOM_SEED,
    )


def _run_dqn(settings, agent):
    return run_env_policy(
        settings,
        action_fn=lambda env, obs: agent.predict(obs, deterministic=True),
        seed=settings.RANDOM_SEED,
    )


def _store_run_result(policy_name, out):
    st.session_state.last_result = {
        "summary": out["summary"],
        "history": out["history"],
        "nodes": out["nodes"],
        "gateway": out["gateway"],
        "policy": policy_name,
        "metrics": out.get("metrics"),
    }


def run_dashboard():
    st.set_page_config(
        page_title="IoT Energy Optimization",
        layout="wide",
    )

    st.title("IoT Energy Optimization")
    st.caption(
        "Simulate IoT nodes, train a DQN agent, and compare energy policies."
    )

    controls = render_controls()
    settings = controls["settings"]
    policy_name = controls["policy_name"]

    if "dqn_agent" not in st.session_state:
        st.session_state.dqn_agent = None
    if "last_result" not in st.session_state:
        st.session_state.last_result = None
    if "comparison" not in st.session_state:
        st.session_state.comparison = None
    if "training_logs" not in st.session_state:
        st.session_state.training_logs = None
        

    model_dir = (Path(settings.MODEL_DIR)/f"nodes_{settings.NUM_NODES}")
    model_dir.mkdir(parents=True,exist_ok=True)

    if controls["train_clicked"]:
        with st.spinner(f"Training DQN for {controls['train_timesteps']} timesteps..."):
            result = train_dqn(
                settings=settings,
                total_timesteps=controls["train_timesteps"],
                model_path=model_dir/settings.MODEL_NAME,
                eval_episodes=5,
                seed=settings.RANDOM_SEED,
            )
        st.session_state.dqn_agent = result["agent"]
        
        # Save training log location
        reward_log_path = (Path("experiments")/f"nodes_{settings.NUM_NODES}"/"reward_log.csv")

        st.session_state.training_logs = {
            "reward_log": reward_log_path
        }
        st.session_state.training_logs = {"reward_log": reward_log_path}        
        st.success(
            f"DQN trained and saved to `{result['model_path']}`. "
            f"Eval mean reward: {result['evaluation']['mean_reward']:.2f}"
        )

    if controls["run_clicked"]:
        if policy_name in ("always_transmit", "always_sleep"):
            out = _run_baseline(settings, policy_name)
            _store_run_result(policy_name, out)
        elif policy_name == "random":
            out = _run_random(settings)
            _store_run_result(policy_name, out)
        elif policy_name == "dqn":
            agent = st.session_state.dqn_agent
            if agent is None:
                model_path = model_dir/settings.MODEL_NAME,
                zip_path = Path(str(model_path) + ".zip")
                if zip_path.exists() or Path(str(model_path)).exists():
                    with st.spinner("Loading saved DQN model..."):
                        agent = DQNAgent.load(
                            model_path,
                            settings=settings,
                            seed=settings.RANDOM_SEED,
                        )
                    st.session_state.dqn_agent = agent
                else:
                    st.warning("No trained DQN found. Click **Train DQN** first.")
                    agent = None
            if agent is not None:
                # Keep agent settings aligned with current UI settings
                agent.settings = settings
                out = _run_dqn(settings, agent)
                _store_run_result(policy_name, out)

    if controls["compare_clicked"]:
        agent = st.session_state.dqn_agent
        with st.spinner("Comparing policies..."):
            st.session_state.comparison = compare_policies(
                settings=settings,
                agent=agent,
                seed=settings.RANDOM_SEED,
                n_episodes=5,
            )
        if agent is None:
            st.info("Compared baselines only. Train DQN to include it in the table.")
        else:
            st.success("Comparison finished (baselines + DQN).")

    result = st.session_state.last_result
    if result is not None:
        st.success(
            f"Finished with policy `{result['policy']}` "
            f"in {result['summary']['steps']} steps."
        )
        render_summary_metrics(result["summary"])

        left, right = st.columns([1.2, 1])
        with left:
            render_history_charts(result["history"])
        
        st.divider()
        st.header("DQN Training Analysis")
        
        if st.session_state.training_logs is not None:

            reward_path = (
                st.session_state.training_logs["reward_log"]
            )


            if reward_path.exists():

                reward_df = pd.read_csv(
                    reward_path
                )

                render_training_reward(
                    reward_df
                )
                
                loss_df = load_tensorboard_loss(
                    "experiments/tensorboard"
                )


                render_dqn_loss(
                    loss_df
                )
                
                render_average_reward(
                        reward_df,
                        window=100
                )

                render_reward_components(
                    reward_df
                )

            else:

                st.info(
                    "Reward log is not available yet."
                )

        else:

            st.info(
                "Train DQN to display training analysis."
            )
        
        
        with right:
            render_network_map(result["nodes"], result["gateway"])
            render_node_table(result["nodes"])
    elif st.session_state.comparison is None:
        st.info(
            "Use the sidebar to **Run Simulation**, **Train DQN**, or **Compare Policies**."
        )

    if st.session_state.comparison is not None:
        st.divider()
        render_comparison(
            st.session_state.comparison["metrics"],
            histories=st.session_state.comparison["histories"],
        )
