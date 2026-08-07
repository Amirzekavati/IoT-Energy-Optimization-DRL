"""
Central gateway that collects packets from IoT nodes.
"""


class Gateway:
    """
    Sink node for the network.

    Lives at a fixed position and stores every successfully received packet.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.received_packets = []

    def receive(self, packet):
        """Accept one packet from a node."""
        packet.mark_delivered()
        self.received_packets.append(packet)
        return True

    def packets_from(self, node_id):
        """Return packets that came from a given node."""
        return [p for p in self.received_packets if p.source_id == node_id]

    def total_received(self):
        return len(self.received_packets)

    def clear(self):
        self.received_packets.clear()

    def __repr__(self):
        return (
            f"Gateway(x={self.x}, y={self.y}, "
            f"received={self.total_received()})"
        )
