"""
Train and evaluate the DQN agent on the IoT energy environment.
"""

from pathlib import Path

from app.config.settings import Settings
from app.rl.dqn_agent import DQNAgent
from app.rl.environment import IoTEnergyEnv

from app.rl.callbacks import RewardLoggerCallback

DEFAULT_MODEL_PATH = Path("experiments/models/dqn_iot_energy")


def evaluate_agent(agent, env=None, n_episodes=5, seed=None):
    """
    Run greedy episodes and return average reward + last summary.
    """
    settings = agent.settings
    eval_env = env or IoTEnergyEnv(settings=settings, seed=seed)
    rewards = []
    last_summary = None

    for episode in range(n_episodes):
        episode_seed = None if seed is None else seed + episode
        obs, info = eval_env.reset(seed=episode_seed)
        done = False
        total_reward = 0.0

        while not done:
            action = agent.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, info = eval_env.step(action)
            total_reward += reward
            done = terminated or truncated

        rewards.append(total_reward)
        last_summary = info.get("summary")

    avg_reward = sum(rewards) / len(rewards) if rewards else 0.0
    return {
        "episode_rewards": rewards,
        "mean_reward": avg_reward,
        "last_summary": last_summary,
    }


def train_dqn(
    settings=None,
    total_timesteps=None,
    model_path=None,
    eval_episodes=5,
    seed=None,
    progress_bar=False,
):
    """
    Train DQN, evaluate it, and save the model.

    Returns a dict with agent path and evaluation metrics.
    """
    settings = settings or Settings()
    seed = settings.RANDOM_SEED if seed is None else seed
    
    if model_path:
        model_path = Path(model_path)
    else:
        model_path = (Path("experiments/models")/f"nodes_{settings.NUM_NODES}"/"dqn_iot_energy")
        
    log_dir = (Path("experiments")/f"nodes_{settings.NUM_NODES}")
    log_dir.mkdir(parents=True,exist_ok=True)
    
    env = IoTEnergyEnv(settings=settings, seed=seed)
    agent = DQNAgent(env=env, settings=settings, seed=seed)
    reward_callback = RewardLoggerCallback(save_path=log_dir/"reward_log.csv")
    agent.learn(total_timesteps=total_timesteps, progress_bar=progress_bar, callback=reward_callback)

    saved_path = agent.save(model_path)
    evaluation = evaluate_agent(
        agent,
        env=IoTEnergyEnv(settings=settings, seed=seed + 1),
        n_episodes=eval_episodes,
        seed=seed + 100,
    )

    return {
        "model_path": str(saved_path),
        "timesteps": total_timesteps or settings.TRAIN_TIMESTEPS,
        "evaluation": evaluation,
        "agent": agent,
    }
