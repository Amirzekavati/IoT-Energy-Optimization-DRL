"""
Compare baseline policies and an optional DQN agent.
"""

from app.analytics.metrics import average_metrics, metrics_from_history
from app.config.settings import Settings
from app.rl.environment import IoTEnergyEnv
from app.simulation.scheduler import AlwaysSleepScheduler, Scheduler
from app.simulation.simulator import Simulator


def run_simulator_policy(settings, scheduler, seed):
    sim = Simulator(settings=settings, scheduler=scheduler, seed=seed)
    history = sim.run()
    summary = sim.summary()
    metrics = metrics_from_history(history, summary, settings)
    return {
        "history": history,
        "summary": summary,
        "metrics": metrics,
        "nodes": sim.nodes,
        "gateway": sim.gateway,
    }


def run_env_policy(settings, action_fn, seed):
    env = IoTEnergyEnv(settings=settings, seed=seed)
    obs, info = env.reset(seed=seed)
    env.action_space.seed(seed)
    history = []
    total_reward = 0.0
    done = False

    while not done:
        action = action_fn(env, obs)
        obs, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
        if info.get("snapshot"):
            history.append(info["snapshot"])
        done = terminated or truncated

    summary = info.get("summary", {})
    metrics = metrics_from_history(history, summary, settings)
    metrics["episode_reward"] = float(total_reward)
    return {
        "history": history,
        "summary": summary,
        "metrics": metrics,
        "nodes": env.simulator.nodes,
        "gateway": env.simulator.gateway,
    }


def evaluate_baselines(settings=None, seed=None, n_episodes=3):
    """
    Evaluate always-transmit, always-sleep, and random policies.
    """
    settings = settings or Settings()
    seed = settings.RANDOM_SEED if seed is None else seed

    policy_runners = {
        "always_transmit": lambda s, ep_seed: run_simulator_policy(
            s, Scheduler(), ep_seed
        ),
        "always_sleep": lambda s, ep_seed: run_simulator_policy(
            s, AlwaysSleepScheduler(), ep_seed
        ),
        "random": lambda s, ep_seed: run_env_policy(
            s,
            action_fn=lambda env, obs: env.action_space.sample(),
            seed=ep_seed,
        ),
    }

    results = {}
    histories = {}

    for name, runner in policy_runners.items():
        episode_metrics = []
        last_history = []
        for episode in range(n_episodes):
            ep_seed = seed + episode
            out = runner(settings, ep_seed)
            episode_metrics.append(out["metrics"])
            last_history = out["history"]
        results[name] = average_metrics(episode_metrics)
        histories[name] = last_history

    return {"metrics": results, "histories": histories}


def evaluate_dqn_agent(agent, settings=None, seed=None, n_episodes=3):
    """Evaluate a trained DQNAgent and return mean metrics + last history."""
    settings = settings or agent.settings
    seed = settings.RANDOM_SEED if seed is None else seed

    episode_metrics = []
    last_history = []

    for episode in range(n_episodes):
        ep_seed = seed + episode

        def action_fn(env, obs, _agent=agent):
            return _agent.predict(obs, deterministic=True)

        out = run_env_policy(settings, action_fn=action_fn, seed=ep_seed)
        episode_metrics.append(out["metrics"])
        last_history = out["history"]

    return {
        "metrics": average_metrics(episode_metrics),
        "history": last_history,
    }


def compare_policies(settings=None, agent=None, seed=None, n_episodes=3):
    """
    Full comparison table: baselines (+ DQN if agent is provided).
    """
    baseline = evaluate_baselines(
        settings=settings,
        seed=seed,
        n_episodes=n_episodes,
    )
    metrics = dict(baseline["metrics"])
    histories = dict(baseline["histories"])

    if agent is not None:
        dqn = evaluate_dqn_agent(
            agent,
            settings=settings,
            seed=(seed if seed is not None else settings.RANDOM_SEED) + 50,
            n_episodes=n_episodes,
        )
        metrics["dqn"] = dqn["metrics"]
        histories["dqn"] = dqn["history"]

    return {"metrics": metrics, "histories": histories}
