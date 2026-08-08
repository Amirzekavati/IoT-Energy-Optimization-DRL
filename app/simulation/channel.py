"""
Lightweight wireless channel helpers.

Kept intentionally simple for a bachelor project:
- distance between node and gateway
- delivery probability decreases with distance
"""

import math


def distance_between(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)


def delivery_probability(distance, settings):
    """
    Higher distance => lower chance the packet arrives.

    p = 1 - LOSS_FACTOR * (d / DISTANCE_REF), clipped to [MIN_DELIVERY_PROB, 1].
    """
    d_ref = max(float(settings.DISTANCE_REF), 1e-6)
    p = 1.0 - float(settings.LOSS_FACTOR) * (float(distance) / d_ref)
    low = float(settings.MIN_DELIVERY_PROB)
    return max(low, min(1.0, p))


def try_deliver(distance, settings, rng):
    """Return True if the packet is successfully delivered."""
    p = delivery_probability(distance, settings)
    return rng.random() < p
