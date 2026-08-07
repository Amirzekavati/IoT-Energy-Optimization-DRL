"""
Charts for simulation history.
"""

import pandas as pd
import streamlit as st


def history_to_dataframe(history):
    if not history:
        return pd.DataFrame(
            columns=[
                "step",
                "alive",
                "total_energy",
                "packets_sent",
                "packets_received",
            ]
        )
    rows = [
        {
            "step": row["step"],
            "alive": row["alive"],
            "total_energy": row["total_energy"],
            "packets_sent": row["packets_sent"],
            "packets_received": row["packets_received"],
        }
        for row in history
    ]
    return pd.DataFrame(rows)


def render_summary_metrics(summary):
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Steps", summary.get("steps", 0))
    col2.metric("Alive nodes", summary.get("alive", 0))
    col3.metric("Packets received", summary.get("packets_received", 0))
    col4.metric("Remaining energy", f"{summary.get('total_energy', 0.0):.3f} J")


def render_history_charts(history):
    df = history_to_dataframe(history)
    if df.empty:
        st.info("No history yet. Run a simulation to see charts.")
        return

    st.subheader("Energy over time")
    st.line_chart(df.set_index("step")[["total_energy"]])

    st.subheader("Alive nodes over time")
    st.line_chart(df.set_index("step")[["alive"]])

    st.subheader("Packets received over time")
    st.line_chart(df.set_index("step")[["packets_received"]])
