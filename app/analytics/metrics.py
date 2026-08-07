"""
Core metrics derived from a simulation run.
"""


def metrics_from_history(history, summary, settings):
    """
    Build a flat metrics dict from simulator history + summary.
    """
    if not history:
        lifetime = 0
        final_energy = summary.get("total_energy", 0.0)
    else:
        # Lifetime = last step index where at least one node was alive,
        # or full run length if nodes survive.
        lifetime = history[-1]["step"] + 1
        for row in history:
            if row["alive"] <= 0:
                lifetime = row["step"] + 1
                break
        final_energy = history[-1]["total_energy"]

    packets = summary.get("packets_received", 0)
    initial_energy = settings.NUM_NODES * settings.INITIAL_ENERGY
    energy_used = max(initial_energy - summary.get("total_energy", 0.0), 0.0)

    energy_efficiency = 0.0
    if energy_used > 0:
        energy_efficiency = packets / energy_used

    pdr = 0.0
    sent = summary.get("packets_sent", 0)
    if sent > 0:
        pdr = packets / sent

    return {
        "lifetime_steps": int(lifetime),
        "alive_final": int(summary.get("alive", 0)),
        "dead_final": int(summary.get("dead", 0)),
        "packets_sent": int(sent),
        "packets_received": int(packets),
        "packet_delivery_ratio": float(pdr),
        "total_energy_final": float(summary.get("total_energy", 0.0)),
        "energy_used": float(energy_used),
        "energy_efficiency": float(energy_efficiency),
        "steps": int(summary.get("steps", 0)),
    }


def average_metrics(metric_list):
    """Average a list of metrics dicts (skips non-numeric safely)."""
    if not metric_list:
        return {}

    keys = metric_list[0].keys()
    result = {}
    for key in keys:
        values = [m[key] for m in metric_list if isinstance(m.get(key), (int, float))]
        result[key] = float(sum(values) / len(values)) if values else 0.0
    return result
