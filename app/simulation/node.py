"""
One IoT sensor node with a limited battery.
"""

import random

from app.simulation.channel import distance_between, try_deliver
from app.simulation.energy_model import EnergyModel
from app.simulation.packet import Packet


class Node:
    """
    States:
      - active: node can sense / transmit
      - sleep:  node saves energy
      - dead:   battery is empty
    """

    def __init__(self, node_id, x, y, initial_energy, energy_model=None):
        self.id = node_id
        self.x = x
        self.y = y
        self.energy = initial_energy
        self.initial_energy = initial_energy
        self.state = "active"
        self.energy_model = energy_model or EnergyModel()

        self.packets_sent = 0
        self.packets_received = 0
        self.packets_dropped = 0
        self.aoi = 0  # Age of Information (steps since last successful delivery)
        self._next_packet_id = 1

    def is_alive(self):
        return self.state != "dead" and self.energy > 0

    def remaining_energy_ratio(self):
        if self.initial_energy <= 0:
            return 0.0
        return max(self.energy, 0.0) / self.initial_energy

    def distance_to(self, gateway):
        return distance_between(self.x, self.y, gateway.x, gateway.y)

    def _use_energy(self, amount):
        """Reduce battery. If energy finishes, mark node as dead."""
        if not self.is_alive():
            return False

        self.energy -= amount
        if self.energy <= 0:
            self.energy = 0.0
            self.state = "dead"
            return False
        return True

    def sense(self):
        """Sense data from the environment."""
        if self.state != "active":
            return False
        return self._use_energy(self.energy_model.sense_cost())

    def create_packet(self, step, size, payload=None):
        """Build a packet after sensing (does not send it yet)."""
        if self.state != "active":
            return None

        packet = Packet(
            packet_id=self._next_packet_id,
            source_id=self.id,
            size=size,
            step=step,
            payload=payload if payload is not None else {"value": float(self.id) + step * 0.1},
        )
        self._next_packet_id += 1
        return packet

    def transmit(self, distance=0.0):
        """Pay the energy cost of sending one packet (distance-aware)."""
        if self.state != "active":
            return False

        ok = self._use_energy(self.energy_model.transmit_cost(distance=distance))
        if ok:
            self.packets_sent += 1
        return ok

    def send_packet(self, gateway, packet, rng=None):
        """
        Transmit one packet to the gateway.

        Energy is always spent on the attempt. Delivery may fail due to distance.
        """
        if packet is None or self.state != "active":
            return False

        distance = self.distance_to(gateway)
        if not self.transmit(distance=distance):
            return False

        rng = rng or random
        if try_deliver(distance, self.energy_model.settings, rng):
            return gateway.receive(packet)

        self.packets_dropped += 1
        return False

    def receive(self):
        """Receive one packet (used by gateway / other nodes later)."""
        if not self.is_alive():
            return False

        ok = self._use_energy(self.energy_model.receive_cost())
        if ok:
            self.packets_received += 1
        return ok

    def sleep(self):
        """Switch to sleep mode for one time step."""
        if not self.is_alive():
            return False

        self.state = "sleep"
        return self._use_energy(self.energy_model.sleep_cost())

    def wake_up(self):
        """Wake up from sleep mode."""
        if self.state == "sleep":
            self.state = "active"
            return True
        return False

    def __repr__(self):
        return (
            f"Node(id={self.id}, energy={self.energy:.4f}, "
            f"state={self.state}, sent={self.packets_sent}, aoi={self.aoi})"
        )
