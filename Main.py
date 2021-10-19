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
        self.PosXarr = []
        self.PosYarr = []
        self.arrowsarr = []
        self.reactiveAgentWorlds = []
        self.P_pit = 0.05
        self.P_obs = 0.05
        self.P_wumpus = 0.05

    def main(self):

        for w in range(10):
            self.agentWorlds.append(WumpWorld(5, self.P_pit, self.P_obs, self.P_wumpus))
            posX, posY, arrows = self.agentWorlds[w].generateProblem()
            self.PosXarr.append(posX)
            self.PosYarr.append(posY)
            self.arrowsarr.append(arrows)
            self.reactiveAgentWorlds.append(self.agentWorlds[w].duplicateProblem())

        for w in range(10):
            self.agentWorlds.append(WumpWorld(10, self.P_pit, self.P_obs, self.P_wumpus))
            posX, posY, arrows = self.agentWorlds[w+10].generateProblem()
            self.PosXarr.append(posX)
            self.PosYarr.append(posY)
            self.arrowsarr.append(arrows)
            self.reactiveAgentWorlds.append(self.agentWorlds[w].duplicateProblem())

        for w in range(10):
            self.agentWorlds.append(WumpWorld(15, self.P_pit, self.P_obs, self.P_wumpus))
            posX, posY, arrows = self.agentWorlds[w+20].generateProblem()
            self.PosXarr.append(posX)
            self.PosYarr.append(posY)
            self.arrowsarr.append(arrows)
            self.reactiveAgentWorlds.append(self.agentWorlds[w].duplicateProblem())

        for w in range(10):
            self.agentWorlds.append(WumpWorld(20, self.P_pit, self.P_obs, self.P_wumpus))
            posX, posY, arrows = self.agentWorlds[w+30].generateProblem()
            self.PosXarr.append(posX)
            self.PosYarr.append(posY)
            self.arrowsarr.append(arrows)
            self.reactiveAgentWorlds.append(self.agentWorlds[w].duplicateProblem())

        for w in range(10):
            self.agentWorlds.append(WumpWorld(25, self.P_pit, self.P_obs, self.P_wumpus))
            posX, posY, arrows = self.agentWorlds[w+40].generateProblem()
            self.PosXarr.append(posX)
            self.PosYarr.append(posY)
            self.arrowsarr.append(arrows)
            self.reactiveAgentWorlds.append(self.agentWorlds[w].duplicateProblem())

        counter = 0
        totalwon = 0
        totalwum = 0
        totalpit = 0
        totalshoot = 0
        totalex = 0
        totalact = 0
        for i in self.agentWorlds:
            a = Agent(i, self.PosXarr[counter], self.PosYarr[counter], self.arrowsarr[counter])
            counter += 1
            won, deadbyWumpus, deadbyPit, wumpusDead, exploredCount, actionCount = a.solve()
            totalwon += won
            totalwum += deadbyWumpus
            totalpit += deadbyPit
            totalshoot += wumpusDead
            totalex += exploredCount
            totalact += actionCount

        print("KNOWLEDGE:")
        print(totalwon, totalwum, totalpit, totalshoot, totalex, totalact)

        counter = 0
        totalwon = 0
        totalwum = 0
        totalpit = 0
        totalshoot = 0
        totalex = 0
        totalact = 0
        for i in self.reactiveAgentWorlds:
            a = Agent(i, self.PosXarr[counter], self.PosYarr[counter], self.arrowsarr[counter])
            counter += 1
            won, deadbyWumpus, deadbyPit, wumpusDead, exploredCount, actionCount = a.solve()
            totalwon += won
            totalwum += deadbyWumpus
            totalpit += deadbyPit
            totalshoot += 0
            totalex += exploredCount
            totalact += actionCount

        print("REACTIVE:")
        print(totalwon, totalwum, totalpit, totalshoot, totalex, totalact)
m = Main()
m.main()