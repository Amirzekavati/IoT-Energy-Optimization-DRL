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
    Creates nodes, applies scheduler decisions, and tracks energy / packets / AoI.
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
        self.packets_dropped = 0
        self.aoi_history = []

        self._rng = random.Random(self.seed)
        self.setup()

    def setup(self):
        """Place nodes randomly inside the simulation area."""
        self.nodes = []
        self.gateway.clear()
        self.current_step = 0
        self.history = []
        self.packets_dropped = 0

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

    def mean_aoi(self):
        alive = self.alive_nodes()
        if not alive:
            return 0.0
        return sum(n.aoi for n in alive) / len(alive)

    def _snapshot(self, actions):
        return {
            "step": self.current_step,
            "alive": len(self.alive_nodes()),
            "total_energy": self.total_energy(),
            "packets_sent": self.packets_sent(),
            "packets_received": self.gateway.total_received(),
            "packets_dropped": self.packets_dropped,
            "mean_aoi": self.mean_aoi(),
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
        before_dropped = node.packets_dropped
        ok = node.send_packet(self.gateway, packet, rng=self._rng)
        if node.packets_dropped > before_dropped:
            # print("PACKET DROP:",node.id,node.packets_dropped)
            self.packets_dropped += 1
        return ok

    def _apply_sleep(self, node):
        """Stay in (or switch to) sleep and pay the sleep energy cost."""
        return node.sleep()

    def _update_aoi(self, delivered_ids):
        """Increase AoI each step; reset when a node successfully delivers."""
        for node in self.nodes:
            if not node.is_alive():
                continue
            if node.id in delivered_ids:
                node.aoi = 1
            else:
                node.aoi += 1

    def step(self, actions=None):
        """
        Run one simulation time step.

        actions: optional dict {node_id: "transmit"|"sleep"}.
                 If None, the scheduler chooses actions.

        Returns a snapshot dict, or None if no alive nodes remain.
        """
        alive = self.alive_nodes()
        if not alive:
            return None

        if actions is None:
            actions = self.scheduler.decide(self.nodes, self.current_step)

        delivered_ids = set()
        for node in alive:
            action = actions.get(node.id, Scheduler.SLEEP)
            if action == Scheduler.TRANSMIT:
                if self._apply_transmit(node):
                    delivered_ids.add(node.id)
            else:
                self._apply_sleep(node)

        self._update_aoi(delivered_ids)

        snapshot = self._snapshot(actions)
        self.aoi_history.append(snapshot["mean_aoi"])
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
        sent = self.packets_sent()
        received = self.gateway.total_received()
        pdr = (received / sent) if sent > 0 else 0.0
        return {
            "steps": self.current_step,
            "alive": len(self.alive_nodes()),
            "dead": len(self.nodes) - len(self.alive_nodes()),
            "total_energy": self.total_energy(),
            "packets_sent": sent,
            "packets_received": received,
            "packets_dropped": self.packets_dropped,
            "packet_delivery_ratio": pdr,
            "mean_aoi": (sum(self.aoi_history) / len(self.aoi_history) if self.aoi_history  else 0.0),
        }

    def __repr__(self):
        return (
            f"Simulator(step={self.current_step}, "
            f"alive={len(self.alive_nodes())}/{len(self.nodes)}, "
            f"received={self.gateway.total_received()}, "
            f"aoi={self.mean_aoi():.1f})"
        )
