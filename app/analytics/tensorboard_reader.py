from pathlib import Path
import pandas as pd

from tensorboard.backend.event_processing.event_accumulator import (
    EventAccumulator
)


def load_tensorboard_loss(log_dir):

    log_dir = Path(log_dir)

    event_files = list(
        log_dir.rglob(
            "events.out.tfevents.*"
        )
    )


    if len(event_files) == 0:
        return None


    event_file = event_files[0]


    accumulator = EventAccumulator(
        str(event_file)
    )

    accumulator.Reload()


    tags = accumulator.Tags()


    if "scalars" not in tags:
        return None


    scalar_tags = tags["scalars"]


    print(
        "Available TensorBoard tags:",
        scalar_tags
    )


    # SB3 usually stores loss here
    loss_tag = None


    for tag in scalar_tags:

        if "loss" in tag.lower():

            loss_tag = tag
            break


    if loss_tag is None:
        return None


    events = accumulator.Scalars(
        loss_tag
    )


    data = []


    for e in events:

        data.append(
            {
                "step": e.step,
                "loss": e.value
            }
        )


    return pd.DataFrame(data)