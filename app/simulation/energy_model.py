"""
Simple energy model for IoT nodes.
"""

from app.config.settings import Settings


class EnergyModel:
    """Returns the energy cost of each node action."""

    def __init__(self, settings=None):
        self.settings = settings or Settings()

    def transmit_cost(self, distance=0.0):
        """
        Base TX cost grows mildly with distance:

            cost = TX_ENERGY * (1 + TX_DISTANCE_WEIGHT * (d / DISTANCE_REF)^2)
        """
        base = self.settings.TX_ENERGY
        d_ref = max(float(self.settings.DISTANCE_REF), 1e-6)
        weight = float(self.settings.TX_DISTANCE_WEIGHT)
        factor = 1.0 + weight * (float(distance) / d_ref) ** 2
        return base * factor

    def receive_cost(self):
        return self.settings.RX_ENERGY

    def sense_cost(self):
        return self.settings.SENSE_ENERGY

    def sleep_cost(self):
        return self.settings.SLEEP_ENERGY
