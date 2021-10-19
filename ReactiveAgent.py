"""
This is an alternative agent that uses less information than regular Agent.
It will be used as a control for comparisons.
"""


class ReactiveAgent:

    def __init__(self, world, x, y):
        self.world = world
        self.pos = [x][y]