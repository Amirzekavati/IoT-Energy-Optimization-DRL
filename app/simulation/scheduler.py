"""
Decides what each node should do in a time step.
"""


class Scheduler:
    """
    Baseline policy: every alive node transmits.

    Later the RL agent will replace this with smarter decisions.
    """

    TRANSMIT = "transmit"
    SLEEP = "sleep"

    def decide(self, nodes, step):
        """
        Return a mapping: node_id -> action.

        Actions:
          - transmit: sense + create packet + send to gateway
          - sleep:    switch to low-power mode for this step
        """
        actions = {}
        for node in nodes:
            if not node.is_alive():
                continue
            actions[node.id] = self.TRANSMIT
        return actions


class AlwaysSleepScheduler(Scheduler):
    """Every alive node sleeps each step (energy-saving baseline)."""

    def decide(self, nodes, step):
        actions = {}
        for node in nodes:
            if not node.is_alive():
                continue
            actions[node.id] = self.SLEEP
        return actions
