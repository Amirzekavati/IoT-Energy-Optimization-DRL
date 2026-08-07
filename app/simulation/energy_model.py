"""
Simple energy model for IoT nodes.

We only track how much energy each action costs.
"""

from app.config.settings import Settings


class EnergyModel:
    """Returns the energy cost of each node action."""

    def __init__(self, settings=None):
        self.settings = settings or Settings()

    def transmit_cost(self):
        return self.settings.TX_ENERGY

    def receive_cost(self):
        return self.settings.RX_ENERGY

    def sense_cost(self):
        return self.settings.SENSE_ENERGY

    def sleep_cost(self):
        return self.settings.SLEEP_ENERGY
