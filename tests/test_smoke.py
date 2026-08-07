"""
End-to-end smoke checks for the IoT Energy Optimization project.

Run:
    python tests/test_smoke.py
"""

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.analytics import compare_policies, comparison_dataframe, metrics_from_history
from app.config.settings import Settings
from app.rl import DQNAgent, IoTEnergyEnv, train_dqn
from app.simulation import AlwaysSleepScheduler, Gateway, Node, Packet, Scheduler, Simulator
from app.ui.charts import history_to_dataframe
from app.ui.dashboard import _run_baseline, _run_dqn, _run_random


class SmokeTests(unittest.TestCase):
    def setUp(self):
        self.settings = Settings()
        self.settings.NUM_NODES = 3
        self.settings.MAX_STEPS = 20
        self.settings.RANDOM_SEED = 7

    def test_node_packet_gateway(self):
        node = Node(1, 10, 20, self.settings.INITIAL_ENERGY)
        gateway = Gateway(self.settings.GATEWAY_X, self.settings.GATEWAY_Y)
        self.assertTrue(node.sense())
        packet = node.create_packet(step=0, size=self.settings.PACKET_SIZE)
        self.assertIsInstance(packet, Packet)
        self.assertTrue(node.send_packet(gateway, packet))
        self.assertEqual(gateway.total_received(), 1)

    def test_simulator_baselines(self):
        tx = Simulator(settings=self.settings, scheduler=Scheduler(), seed=1)
        tx.run()
        self.assertGreater(tx.summary()["packets_received"], 0)

        sleep = Simulator(
            settings=self.settings,
            scheduler=AlwaysSleepScheduler(),
            seed=1,
        )
        sleep.run()
        self.assertEqual(sleep.summary()["packets_received"], 0)
        self.assertGreater(sleep.summary()["total_energy"], tx.summary()["total_energy"])

    def test_rl_env_random_episode(self):
        env = IoTEnergyEnv(settings=self.settings, seed=1)
        obs, info = env.reset()
        self.assertEqual(obs.shape[0], 2 * self.settings.NUM_NODES + 2)
        total = 0.0
        for _ in range(self.settings.MAX_STEPS):
            obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
            total += reward
            if terminated or truncated:
                break
        self.assertTrue(info["summary"]["steps"] > 0)
        self.assertIsInstance(total, float)

    def test_short_dqn_train_and_compare(self):
        result = train_dqn(
            settings=self.settings,
            total_timesteps=800,
            model_path=ROOT / "experiments" / "models" / "dqn_smoke_test",
            eval_episodes=1,
            seed=1,
        )
        agent = result["agent"]
        self.assertTrue(Path(str(result["model_path"]) + ".zip").exists() or Path(result["model_path"]).exists())

        loaded = DQNAgent.load(result["model_path"], settings=self.settings, seed=1)
        self.assertIsNotNone(loaded.predict)

        comparison = compare_policies(
            settings=self.settings,
            agent=agent,
            seed=1,
            n_episodes=1,
        )
        df = comparison_dataframe(comparison["metrics"])
        self.assertIn("dqn", set(df["policy"]))
        self.assertIn("always_transmit", set(df["policy"]))

    def test_dashboard_helpers_and_metrics(self):
        out = _run_baseline(self.settings, "always_transmit")
        metrics = metrics_from_history(out["history"], out["summary"], self.settings)
        self.assertGreater(metrics["packets_received"], 0)
        self.assertFalse(history_to_dataframe(out["history"]).empty)

        out_sleep = _run_baseline(self.settings, "always_sleep")
        self.assertEqual(out_sleep["summary"]["packets_received"], 0)

        out_random = _run_random(self.settings)
        self.assertIn("nodes", out_random)

        # Tiny agent path for DQN helper
        result = train_dqn(
            settings=self.settings,
            total_timesteps=400,
            model_path=ROOT / "experiments" / "models" / "dqn_smoke_ui",
            eval_episodes=1,
            seed=2,
        )
        out_dqn = _run_dqn(self.settings, result["agent"])
        self.assertIn("gateway", out_dqn)


if __name__ == "__main__":
    unittest.main(verbosity=2)
