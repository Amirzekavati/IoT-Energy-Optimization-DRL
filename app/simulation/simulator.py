"""
Runs the IoT network simulation step by step.
"""

import random

from app.config.settings import Settings
from app.simulation.energy_model import EnergyModel
from app.simulation.gateway import Gateway
from app.simulation.node import Node
from app.simulation.scheduler import Scheduler


class Simulator:
    """
    Creates nodes, applies scheduler decisions, and tracks energy / packets.
    """

    def __init__(self, settings=None, scheduler=None, seed=None):
        self.settings = settings or Settings()
        self.scheduler = scheduler or Scheduler()
        self.seed = self.settings.RANDOM_SEED if seed is None else seed

        self.energy_model = EnergyModel(self.settings)
        self.gateway = Gateway(self.settings.GATEWAY_X, self.settings.GATEWAY_Y)
        self.nodes = []
        self.current_step = 0
        self.history = []

        self._rng = random.Random(self.seed)
        self.setup()

    def setup(self):
        """Place nodes randomly inside the simulation area."""
        self.nodes = []
        self.gateway.clear()
        self.current_step = 0
        self.history = []

        for node_id in range(1, self.settings.NUM_NODES + 1):
            x = self._rng.uniform(0.0, self.settings.AREA_SIZE)
            y = self._rng.uniform(0.0, self.settings.AREA_SIZE)
            node = Node(
                node_id=node_id,
                x=x,
                y=y,
                initial_energy=self.settings.INITIAL_ENERGY,
                energy_model=self.energy_model,
            )
            self.nodes.append(node)

    def alive_nodes(self):
        return [n for n in self.nodes if n.is_alive()]

    def total_energy(self):
        return sum(n.energy for n in self.nodes)

    def packets_sent(self):
        return sum(n.packets_sent for n in self.nodes)

    def _snapshot(self, actions):
        return {
            "step": self.current_step,
            "alive": len(self.alive_nodes()),
            "total_energy": self.total_energy(),
            "packets_sent": self.packets_sent(),
            "packets_received": self.gateway.total_received(),
            "actions": dict(actions),
        }

    def _apply_transmit(self, node):
        """Wake if needed, sense, create packet, send to gateway."""
        if node.state == "sleep":
            node.wake_up()

        if not node.sense():
            return False

        packet = node.create_packet(
            step=self.current_step,
            size=self.settings.PACKET_SIZE,
        )
        return node.send_packet(self.gateway, packet)

    def _apply_sleep(self, node):
        """Stay in (or switch to) sleep and pay the sleep energy cost."""
        return node.sleep()

    def step(self):
        """
        Run one simulation time step.

        Returns a snapshot dict, or None if no alive nodes remain.
        """
        alive = self.alive_nodes()
        if not alive:
            return None

        actions = self.scheduler.decide(self.nodes, self.current_step)

        for node in alive:
            action = actions.get(node.id, Scheduler.SLEEP)
            if action == Scheduler.TRANSMIT:
                self._apply_transmit(node)
            else:
                self._apply_sleep(node)

        snapshot = self._snapshot(actions)
        self.history.append(snapshot)
        self.current_step += 1
        return snapshot

    def run(self, max_steps=None):
        """
        Run until max_steps or until all nodes are dead.

        Returns the history list.
        """
        limit = max_steps if max_steps is not None else self.settings.MAX_STEPS

        while self.current_step < limit:
            if self.step() is None:
                break

        return self.history

    def summary(self):
        """Compact result after a run."""
        return {
            "steps": self.current_step,
            "alive": len(self.alive_nodes()),
            "dead": len(self.nodes) - len(self.alive_nodes()),
            "total_energy": self.total_energy(),
            "packets_sent": self.packets_sent(),
            "packets_received": self.gateway.total_received(),
        }

    def __repr__(self):
        return (
            f"Simulator(step={self.current_step}, "
            f"alive={len(self.alive_nodes())}/{len(self.nodes)}, "
            f"received={self.gateway.total_received()})"
        )
