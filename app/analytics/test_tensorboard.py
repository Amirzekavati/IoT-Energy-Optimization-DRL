from app.analytics.tensorboard_reader import load_tensorboard_loss


df = load_tensorboard_loss(
    "experiments/tensorboard"
)


print(df.head())