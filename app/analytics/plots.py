"""
Matplotlib helpers for evaluation charts.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def comparison_dataframe(results):
    """
    results: dict[str, metrics_dict]
    """
    rows = []
    for name, metrics in results.items():
        row = {"policy": name}
        row.update(metrics)
        rows.append(row)
    return pd.DataFrame(rows)


def plot_metric_bars(results, metric_key, title=None, ylabel=None, ax=None):
    """Bar chart comparing one metric across policies."""
    df = comparison_dataframe(results)
    own_ax = ax is None
    if own_ax:
        _, ax = plt.subplots(figsize=(7, 4))

    ax.bar(df["policy"], df[metric_key], color="#3B7DDD")
    ax.set_title(title or metric_key)
    ax.set_ylabel(ylabel or metric_key)
    ax.tick_params(axis="x", rotation=20)
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    if own_ax:
        plt.tight_layout()
    return ax


def plot_comparison_grid(results, save_path=None):
    """
    Four key charts: lifetime, packets, remaining energy, efficiency.
    """
    fig, axes = plt.subplots(2, 2, figsize=(10, 7))
    specs = [
        ("lifetime_steps", "Network lifetime (steps)", "Steps"),
        ("packets_received", "Packets received", "Packets"),
        ("total_energy_final", "Remaining energy", "Joules"),
        ("energy_efficiency", "Energy efficiency (pkt / J)", "pkt / J"),
    ]

    for ax, (key, title, ylabel) in zip(axes.ravel(), specs):
        plot_metric_bars(results, key, title=title, ylabel=ylabel, ax=ax)

    fig.suptitle("Policy comparison", fontsize=14)
    fig.tight_layout()

    if save_path is not None:
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=150, bbox_inches="tight")

    return fig


def plot_energy_curves(histories, save_path=None):
    """
    histories: dict[str, list[snapshot]]
    """
    fig, ax = plt.subplots(figsize=(8, 4))
    for name, history in histories.items():
        if not history:
            continue
        steps = [row["step"] for row in history]
        energy = [row["total_energy"] for row in history]
        ax.plot(steps, energy, label=name)

    ax.set_title("Total energy over time")
    ax.set_xlabel("Step")
    ax.set_ylabel("Energy (J)")
    ax.legend()
    ax.grid(linestyle="--", alpha=0.4)
    fig.tight_layout()

    if save_path is not None:
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=150, bbox_inches="tight")

    return fig
