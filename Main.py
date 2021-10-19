"""
Core experiment manager that instantiates the other classes.
Statistics will be tracked here.
"""
from WumpWorld import *
from Agent import *


class Main:
    def __init__(self):
        self.agentWorlds = []
        self.reactiveAgentWorlds = []
        self.P_pit = 0.10
        self.P_obs = 0.10
        self.P_wumpus = 0.10

    def main(self):
        for w in range(1):
            self.agentWorlds.append(WumpWorld(5, self.P_pit, self.P_obs, self.P_wumpus))
        for a in self.agentWorlds:
            self.reactiveAgentWorlds.append(a.duplicateProblem)

        self.agentWorlds[0].printWorld()
        self.reactiveAgentWorlds[0].printWorld()


m = Main()
Main.main()