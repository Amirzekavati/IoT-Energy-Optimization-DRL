"""
Project settings.

All important numbers live here so we can change them in one place.
"""


class Settings:
    # --- Network ---
    NUM_NODES = 10
    AREA_SIZE = 100.0  # meters (square area: AREA_SIZE x AREA_SIZE)
    GATEWAY_X = 50.0  # center of the area by default
    GATEWAY_Y = 50.0

    # --- Energy (Joules) ---
    INITIAL_ENERGY = 1.0
    TX_ENERGY = 0.05  # energy used to transmit one packet
    RX_ENERGY = 0.02  # energy used to receive one packet
    SENSE_ENERGY = 0.01  # energy used to sense data
    SLEEP_ENERGY = 0.001  # energy used while sleeping (one time step)

    # --- Simulation ---
    MAX_STEPS = 200
    PACKET_SIZE = 32  # bytes (kept simple for now)
    RANDOM_SEED = 42

    # --- Lightweight realism (distance / channel / AoI) ---
    DISTANCE_REF = 50.0  # meters; reference distance for TX cost and loss
    TX_DISTANCE_WEIGHT = 0.5  # how strongly distance increases TX energy
    LOSS_FACTOR = 0.35  # higher => more packet loss with distance
    MIN_DELIVERY_PROB = 0.45  # never drop below this probability
    AOI_REWARD_WEIGHT = 0.15  # penalty weight for average Age of Information

    # --- RL ---
    LEARNING_RATE = 5e-4
    GAMMA = 0.99
    TRAIN_TIMESTEPS = 10000
    MODEL_DIR = "experiments/models"
    MODEL_NAME = "dqn_iot_energy"
