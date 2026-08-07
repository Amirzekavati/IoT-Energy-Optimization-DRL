"""
Reward shaping for the IoT energy RL environment.
"""


def compute_reward(prev_snapshot, next_snapshot, settings):
    """
    Encourage packet delivery and network lifetime.

    Positive:
      - new packets delivered to the gateway
      - nodes still alive
      - remaining energy
    Negative:
      - energy spent this step
      - nodes that died this step
    """
    new_packets = next_snapshot["packets_received"] - prev_snapshot["packets_received"]
    energy_spent = prev_snapshot["total_energy"] - next_snapshot["total_energy"]
    died = prev_snapshot["alive"] - next_snapshot["alive"]

    alive_ratio = 0.0
    if settings.NUM_NODES > 0:
        alive_ratio = next_snapshot["alive"] / settings.NUM_NODES

    energy_ratio = 0.0
    max_energy = settings.NUM_NODES * settings.INITIAL_ENERGY
    if max_energy > 0:
        energy_ratio = next_snapshot["total_energy"] / max_energy

    reward = 0.0
    reward += 1.0 * new_packets
    reward += 0.2 * alive_ratio
    reward += 0.2 * energy_ratio
    reward -= 0.5 * max(energy_spent, 0.0)
    reward -= 1.0 * max(died, 0)

    return float(reward)
