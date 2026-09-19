"""
Reward shaping for the IoT energy RL environment.
"""


def compute_reward_details(prev_snapshot, next_snapshot, settings):
    """
    Reward function for IoT energy optimization using DQN.

    Positive rewards:
        - Packet delivery
        - Remaining energy
        - Network lifetime

    Negative penalties:
        - AoI (information aging)
        - Energy consumption
        - Node death
        - Packet drops
    """

    # ============================
    # Raw changes
    # ============================

    new_packets = (
        next_snapshot["packets_received"]
        -
        prev_snapshot["packets_received"]
    )

    energy_spent = (
        prev_snapshot["total_energy"]
        -
        next_snapshot["total_energy"]
    )

    died = (
        prev_snapshot["alive"]
        -
        next_snapshot["alive"]
    )

    new_drops = (
        next_snapshot.get("packets_dropped", 0)
        -
        prev_snapshot.get("packets_dropped", 0)
    )


    # ============================
    # Normalized metrics
    # ============================

    # Alive node ratio

    alive_ratio = 0.0

    if settings.NUM_NODES > 0:
        alive_ratio = (
            next_snapshot["alive"]
            /
            settings.NUM_NODES
        )


    # Remaining energy ratio

    max_energy = (
        settings.NUM_NODES
        *
        settings.INITIAL_ENERGY
    )

    energy_ratio = 0.0

    if max_energy > 0:
        energy_ratio = (
            next_snapshot["total_energy"]
            /
            max_energy
        )


    # Packet delivery ratio

    max_possible_packets = max(
        settings.NUM_NODES,
        1
    )

    packet_ratio = (
        new_packets
        /
        max_possible_packets
    )


    # Energy consumption ratio

    energy_consumption_ratio = 0.0

    if max_energy > 0:
        energy_consumption_ratio = (
            max(energy_spent, 0.0)
            /
            max_energy
        )


    # Node death ratio

    death_ratio = (
        max(died, 0)
        /
        max(settings.NUM_NODES, 1)
    )


    # Packet drop ratio

    drop_ratio = (
        max(new_drops, 0)
        /
        max(settings.NUM_NODES, 1)
    )


    # AoI normalization

    mean_aoi = float(
        next_snapshot.get(
            "mean_aoi",
            0.0
        )
    )

    aoi_norm = (
        mean_aoi
        /
        max(
            float(settings.MAX_STEPS),
            1.0
        )
    )


    # ============================
    # Positive reward components
    # ============================

    # Weights:
    # Packet Delivery = 0.55
    # Energy          = 0.25
    # Lifetime        = 0.20
    #
    # Sum = 1


    packet_reward = (
        0.55
        *
        packet_ratio
    )


    energy_reward = (
        0.25
        *
        energy_ratio
    )


    alive_reward = (
        0.20
        *
        alive_ratio
    )


    # ============================
    # Negative penalty components
    # ============================

    aoi_penalty = (
        -0.10
        *
        aoi_norm
    )


    energy_penalty = (
        -0.05
        *
        energy_consumption_ratio
    )


    death_penalty = (
        -0.20
        *
        death_ratio
    )


    drop_penalty = (
        -0.05
        *
        drop_ratio
    )


    # ============================
    # Total reward
    # ============================

    total_reward = (
        packet_reward
        +
        energy_reward
        +
        alive_reward
        +
        aoi_penalty
        +
        energy_penalty
        +
        death_penalty
        +
        drop_penalty
    )


    return {

        # Raw information

        "new_packets": new_packets,

        "energy_spent": energy_spent,

        "nodes_died": died,

        "new_drops": new_drops,


        # Normalized metrics

        "packet_ratio": packet_ratio,

        "energy_ratio": energy_ratio,

        "energy_consumption_ratio": energy_consumption_ratio,

        "alive_ratio": alive_ratio,

        "death_ratio": death_ratio,

        "drop_ratio": drop_ratio,

        "aoi_norm": aoi_norm,


        # Reward components

        "packet_reward": packet_reward,

        "energy_reward": energy_reward,

        "alive_reward": alive_reward,

        "aoi_penalty": aoi_penalty,

        "energy_penalty": energy_penalty,

        "death_penalty": death_penalty,

        "drop_penalty": drop_penalty,


        # Final reward

        "total_reward": float(total_reward)
    }



def compute_reward(prev_snapshot, next_snapshot, settings):
    """
    Compute scalar reward used by DQN training.
    """

    details = compute_reward_details(
        prev_snapshot,
        next_snapshot,
        settings
    )

    return float(
        details["total_reward"]
    )