"""
Node table and network map for the dashboard.
"""

import altair as alt
import pandas as pd
import streamlit as st


def nodes_to_dataframe(nodes):
    rows = []
    for node in nodes:
        rows.append(
            {
                "id": node.id,
                "x": round(node.x, 2),
                "y": round(node.y, 2),
                "energy": round(node.energy, 4),
                "energy_ratio": round(node.remaining_energy_ratio(), 3),
                "state": node.state,
                "packets_sent": node.packets_sent,
            }
        )
    return pd.DataFrame(rows)


def render_node_table(nodes):
    st.subheader("Nodes")
    df = nodes_to_dataframe(nodes)
    if df.empty:
        st.write("No nodes.")
        return
    st.dataframe(df, use_container_width=True)


def render_network_map(nodes, gateway):
    """Scatter map of nodes and the gateway."""
    st.subheader("Network map")

    rows = []
    for node in nodes:
        rows.append(
            {
                "x": node.x,
                "y": node.y,
                "label": f"N{node.id}",
                "kind": node.state,
            }
        )
    rows.append(
        {
            "x": gateway.x,
            "y": gateway.y,
            "label": "GW",
            "kind": "gateway",
        }
    )
    df = pd.DataFrame(rows)

    chart = (
        alt.Chart(df)
        .mark_circle(size=120)
        .encode(
            x=alt.X("x:Q", title="X (m)"),
            y=alt.Y("y:Q", title="Y (m)"),
            color=alt.Color("kind:N", title="Type / state"),
            tooltip=["label", "kind", "x", "y"],
        )
        .properties(height=360)
    )
    st.altair_chart(chart, use_container_width=True)
