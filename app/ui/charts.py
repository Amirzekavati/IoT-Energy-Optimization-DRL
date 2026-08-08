"""
Charts for simulation history and policy comparison.
"""

import pandas as pd
import streamlit as st

from app.analytics.plots import comparison_dataframe


def history_to_dataframe(history):
    if not history:
        return pd.DataFrame(
            columns=[
                "step",
                "alive",
                "total_energy",
                "packets_sent",
                "packets_received",
                "mean_aoi",
            ]
        )
    rows = [
        {
            "step": row["step"],
            "alive": row["alive"],
            "total_energy": row["total_energy"],
            "packets_sent": row["packets_sent"],
            "packets_received": row["packets_received"],
            "mean_aoi": row.get("mean_aoi", 0.0),
        }
        for row in history
    ]
    return pd.DataFrame(rows)


def render_summary_metrics(summary):
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Steps", summary.get("steps", 0))
    col2.metric("Alive nodes", summary.get("alive", 0))
    col3.metric("Packets received", summary.get("packets_received", 0))
    col4.metric("PDR", f"{summary.get('packet_delivery_ratio', 0.0):.2f}")
    col5.metric("Mean AoI", f"{summary.get('mean_aoi', 0.0):.1f}")


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

    if "mean_aoi" in df.columns:
        st.subheader("Mean Age of Information over time")
        st.line_chart(df.set_index("step")[["mean_aoi"]])


def render_comparison(metrics_by_policy, histories=None):
    """Show comparison table and simple bar charts."""
    st.subheader("Policy comparison")
    df = comparison_dataframe(metrics_by_policy)
    if df.empty:
        st.info("No comparison results yet.")
        return

    show_cols = [
        c
        for c in [
            "policy",
            "lifetime_steps",
            "packets_received",
            "packet_delivery_ratio",
            "mean_aoi",
            "total_energy_final",
            "energy_efficiency",
            "episode_reward",
        ]
        if c in df.columns
    ]
    st.dataframe(df[show_cols], use_container_width=True)

    # Separate charts so different units are not stacked misleadingly
    for col, title in [
        ("lifetime_steps", "Lifetime"),
        ("packets_received", "Packets received"),
        ("mean_aoi", "Mean AoI"),
        ("packet_delivery_ratio", "PDR"),
    ]:
        if col in df.columns:
            st.caption(title)
            st.bar_chart(df.set_index("policy")[[col]])

    if histories:
        energy_rows = []
        for name, history in histories.items():
            for row in history:
                energy_rows.append(
                    {
                        "step": row["step"],
                        "policy": name,
                        "total_energy": row["total_energy"],
                    }
                )
        if energy_rows:
            energy_df = pd.DataFrame(energy_rows)
            pivot = energy_df.pivot_table(
                index="step",
                columns="policy",
                values="total_energy",
                aggfunc="first",
            )
            st.subheader("Energy over time by policy")
            st.line_chart(pivot)
