"""
A data packet sent from an IoT node to the gateway.
"""


class Packet:
    """One unit of sensed data moving through the network."""

    def __init__(self, packet_id, source_id, size, step, payload=None):
        self.id = packet_id
        self.source_id = source_id
        self.size = size  # bytes
        self.step = step  # simulation time step when created
        self.payload = payload if payload is not None else {}
        self.delivered = False

    def mark_delivered(self):
        self.delivered = True

    def __repr__(self):
        return (
            f"Packet(id={self.id}, src={self.source_id}, "
            f"size={self.size}B, step={self.step}, delivered={self.delivered})"
        )
