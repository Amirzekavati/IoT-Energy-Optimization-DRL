from stable_baselines3.common.callbacks import BaseCallback
import pandas as pd
from pathlib import Path


class RewardLoggerCallback(BaseCallback):

    def __init__(
        self,
        save_path="experiments/reward_log.csv",
        verbose=0
    ):
        super().__init__(verbose)
        self.save_path = Path(save_path)
        self.logs = []


    def _on_step(self):

        env = self.training_env.envs[0].unwrapped

        if len(env.reward_history) > 0:

            latest_reward = (
                env.reward_history[-1]
            )

            latest_reward["step"] = (
                self.num_timesteps
            )

            self.logs.append(
                latest_reward.copy()
            )

        return True


    def _on_training_end(self):

        self.save_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        df = pd.DataFrame(
            self.logs
        )

        df.to_csv(
            self.save_path,
            index=False
        )