"""
Core experiment manager that instantiates the other classes.
Statistics will be tracked here.
"""
from WumpWorld import *
from Agent import *
from ReactiveAgent import *


class Main:
    def __init__(self):
        self.agentWorlds = []
        self.reactiveAgentWorlds = []
        self.P_pit = 0.10
        self.P_obs = 0.10
        self.P_wumpus = 0.10

    def main(self):

        size = 5
        for w in range(1):
            self.agentWorlds.append(WumpWorld(size, self.P_pit, self.P_obs, self.P_wumpus))
            posX, posY, arrows = self.agentWorlds[0].generateProblem()
            self.reactiveAgentWorlds.append(self.agentWorlds[w].duplicateProblem())

        #a = Agent(self.agentWorlds[0], posX, posY, arrows)
        b = ReactiveAgent(self.agentWorlds[0], posX, posY, arrows)
        self.agentWorlds[0].printWorld(posX, posY)

        won, deadbyWumpus, deadbyPit, wumpusDead, exploredCount, actionCount = b.solve()
        print(won, deadbyWumpus, deadbyPit, wumpusDead, exploredCount, actionCount)

m = Main()
m.main()