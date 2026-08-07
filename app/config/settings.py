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

    # --- RL (used later) ---
    LEARNING_RATE = 0.001
    GAMMA = 0.95
    TRAIN_TIMESTEPS = 10000
