"""
Main Streamlit dashboard page.
"""

import streamlit as st

from app.simulation import AlwaysSleepScheduler, Scheduler, Simulator
from app.ui.charts import render_history_charts, render_summary_metrics
from app.ui.controls import render_controls
from app.ui.node_manager import render_network_map, render_node_table


def _build_scheduler(policy_name):
    if policy_name == "always_sleep":
        return AlwaysSleepScheduler()
    return Scheduler()


def run_dashboard():
    st.set_page_config(
        page_title="IoT Energy Optimization",
        layout="wide",
    )

    st.title("IoT Energy Optimization")
    st.caption(
        "Simulate IoT nodes with limited battery and compare baseline sleep/transmit policies."
    )

    settings, policy_name, run_clicked = render_controls()

    if "last_result" not in st.session_state:
        st.session_state.last_result = None

    if run_clicked:
        simulator = Simulator(
            settings=settings,
            scheduler=_build_scheduler(policy_name),
            seed=settings.RANDOM_SEED,
        )
        simulator.run()
        st.session_state.last_result = {
            "summary": simulator.summary(),
            "history": simulator.history,
            "nodes": simulator.nodes,
            "gateway": simulator.gateway,
            "policy": policy_name,
        }

    result = st.session_state.last_result
    if result is None:
        st.info("Set parameters in the sidebar, then click **Run Simulation**.")
        return

    st.success(
        f"Finished with policy `{result['policy']}` "
        f"in {result['summary']['steps']} steps."
    )
    render_summary_metrics(result["summary"])

    left, right = st.columns([1.2, 1])
    with left:
        render_history_charts(result["history"])
    with right:
        render_network_map(result["nodes"], result["gateway"])
        render_node_table(result["nodes"])
