from WumpWorld import *

class Agent:

    #initialize instance of agent
    def __init__(self, world):
        self.world = WumpWorld
        self.arrows = 0
        self.wumpusAlive = 0
        self.frontierCells = 0
        self.safeCells = 0
        self.pathingRoute = 0
        self.boardKnowledge = 0
        self.posX = 0
        self.posY = 0
        self.direction = 0
        self.dead = False
        self.won = False
        self.rules = []
        self.populateRules()

    #populate rules [] with all the rules we are defining
    def populateRules(self):
        # if no sense, all adjacent cells are safe

        # if stench, atleast one adjcaent cell has wumpus
        # if breeze, atleast one adjacent cell has pit
        # if scream, wumpus has died
        pass

    #update knowledge base based on a single rule
    def updateKnowldge(self, rule):
        pass

    # iterate through all the rules and update each one until nothing else can be updated with new knowledge
    def inferenceSystem(self):
        updated = True
        while updated:
            updated = False
            for rule in self.rules:
                if self.updateKnowledge(rule):
                    updated = True


    def takeAction(self):
        percept = self.world.perceiveCell(self.posX, self.posY)
        if percept == "glitter":
            self.won == True
            return "Won"
        if percept == "wumpus" or percept == "pit":
            self.dead == True
            return "Dead"
        
        pass

    def generateRoute(self):
        pass