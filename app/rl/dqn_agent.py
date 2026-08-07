"""
DQN agent built on Stable-Baselines3.
"""

from pathlib import Path

from gymnasium import spaces
from stable_baselines3 import DQN

from app.config.settings import Settings
from app.rl.environment import IoTEnergyEnv


class DQNAgent:
    """Thin wrapper around SB3 DQN for this project."""

    def __init__(self, env=None, settings=None, seed=None):
        self.settings = settings or Settings()
        self.seed = seed if seed is not None else self.settings.RANDOM_SEED
        self.env = env or IoTEnergyEnv(settings=self.settings, seed=self.seed)

        if not isinstance(self.env.action_space, spaces.Discrete):
            raise ValueError(
                "DQN needs a Discrete action space. "
                "Use NUM_NODES <= 10 in Settings."
            )

        self.model = DQN(
            policy="MlpPolicy",
            env=self.env,
            learning_rate=self.settings.LEARNING_RATE,
            gamma=self.settings.GAMMA,
            buffer_size=50_000,
            learning_starts=1_000,
            batch_size=64,
            tau=1.0,
            train_freq=4,
            target_update_interval=500,
            exploration_fraction=0.3,
            exploration_final_eps=0.05,
            verbose=0,
            seed=self.seed,
        )

    def learn(self, total_timesteps=None, progress_bar=False):
        timesteps = (
            self.settings.TRAIN_TIMESTEPS
            if total_timesteps is None
            else total_timesteps
        )
        self.model.learn(total_timesteps=timesteps, progress_bar=progress_bar)
        return self

    def predict(self, observation, deterministic=True):
        action, _state = self.model.predict(
            observation,
            deterministic=deterministic,
        )
        return action

    def save(self, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.model.save(str(path))
        return path

    @classmethod
    def load(cls, path, env=None, settings=None, seed=None):
        agent = cls.__new__(cls)
        agent.settings = settings or Settings()
        agent.seed = seed if seed is not None else agent.settings.RANDOM_SEED
        agent.env = env or IoTEnergyEnv(settings=agent.settings, seed=agent.seed)
        agent.model = DQN.load(str(path), env=agent.env)
        return agent
