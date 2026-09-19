"""
Gymnasium environment wrapping the IoT network simulator.
"""

import numpy as np
import gymnasium as gym
from gymnasium import spaces

from app.config.settings import Settings
from app.rl.reward import (
    compute_reward,
    compute_reward_details
)
from app.simulation.scheduler import Scheduler
from app.simulation.simulator import Simulator


class IoTEnergyEnv(gym.Env):
    """
    Each step, the agent chooses transmit(1) or sleep(0) for every node.

    Observation (Box, shape = 2 * num_nodes + 3):
      - energy ratio per node
      - alive flag per node (1/0)
      - normalized simulation step
      - gateway receive ratio (received / max possible so far)
      - normalized mean Age of Information

    Action:
      - Discrete(2 ** num_nodes) when num_nodes <= 10 (DQN-friendly)
      - MultiDiscrete([2] * num_nodes) otherwise
    """

    metadata = {"render_modes": []}

    def __init__(self, settings=None, seed=None):
        super().__init__()
        self.settings = settings or Settings()
        self._seed = seed if seed is not None else self.settings.RANDOM_SEED
        self.num_nodes = self.settings.NUM_NODES

        obs_dim = 2 * self.num_nodes + 3
        self.observation_space = spaces.Box(
            low=0.0,
            high=1.0,
            shape=(obs_dim,),
            dtype=np.float32,
        )

        if self.num_nodes <= 10:
            self._flat_actions = True
            self.action_space = spaces.Discrete(2 ** self.num_nodes)
        else:
            self._flat_actions = False
            self.action_space = spaces.MultiDiscrete(
                np.array([2] * self.num_nodes, dtype=np.int64)
            )

        self.simulator = None
        self._prev_snapshot = None
        
        self.reward_history = []

    def _decode_action(self, action):
        """Convert env action to {node_id: transmit|sleep}."""
        bits = []
        if self._flat_actions:
            value = int(action)
            for i in range(self.num_nodes):
                bits.append((value >> i) & 1)
        else:
            bits = [int(x) for x in action]

        actions = {}
        for node, bit in zip(self.simulator.nodes, bits):
            actions[node.id] = (
                Scheduler.TRANSMIT if bit == 1 else Scheduler.SLEEP
            )
        return actions

    def _get_obs(self):
        energy = []
        alive = []
        for node in self.simulator.nodes:
            energy.append(node.remaining_energy_ratio())
            alive.append(1.0 if node.is_alive() else 0.0)

        step_norm = 0.0
        if self.settings.MAX_STEPS > 0:
            step_norm = min(
                self.simulator.current_step / self.settings.MAX_STEPS,
                1.0,
            )

        max_packets = max(self.simulator.current_step * self.num_nodes, 1)
        receive_ratio = self.simulator.gateway.total_received() / max_packets
        receive_ratio = float(np.clip(receive_ratio, 0.0, 1.0))

        aoi_norm = self.simulator.mean_aoi() / max(float(self.settings.MAX_STEPS), 1.0)
        aoi_norm = float(np.clip(aoi_norm, 0.0, 1.0))

        obs = np.asarray(
            energy + alive + [step_norm, receive_ratio, aoi_norm],
            dtype=np.float32,
        )
        return obs

    def _empty_snapshot(self):
        return {
            "step": self.simulator.current_step,
            "alive": len(self.simulator.alive_nodes()),
            "total_energy": self.simulator.total_energy(),
            "packets_sent": self.simulator.packets_sent(),
            "packets_received": self.simulator.gateway.total_received(),
            "packets_dropped": self.simulator.packets_dropped,
            "mean_aoi": self.simulator.mean_aoi(),
            "actions": {},
        }

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        if seed is not None:
            self._seed = seed

        self.simulator = Simulator(settings=self.settings, seed=self._seed)
        self._prev_snapshot = self._empty_snapshot()
        self.reward_history = []
        info = {"summary": self.simulator.summary()}
        return self._get_obs(), info

    def step(self, action):
        if self.simulator is None:
            raise RuntimeError("Call reset() before step().")

        prev = self._prev_snapshot
        actions = self._decode_action(action)
        snapshot = self.simulator.step(actions=actions)

        terminated = snapshot is None or len(self.simulator.alive_nodes()) == 0
        truncated = self.simulator.current_step >= self.settings.MAX_STEPS

        if snapshot is None:
            snapshot = self._empty_snapshot()

        reward = compute_reward(prev, snapshot, self.settings)
        reward_details = compute_reward_details(prev, snapshot, self.settings)
        self.reward_history.append(reward_details)
        self._prev_snapshot = snapshot

        obs = self._get_obs()
        info = {
            "summary": self.simulator.summary(),
            "snapshot": snapshot,
        }
        return obs, reward, terminated, truncated, info
