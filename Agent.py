
class Agent:
    def __init__(self):
        self.arrows = 0
        self.wumpusAlive = 0
        self.frontierCells = 0
        self.safeCells = 0
        self.pathingRoute = 0
        self.boardKnowledge = 0
        self.rules = []

    def updateKnowldge(self):
        pass

    def inferenceSystem(self):
        updated = True
        while updated:
            updated = False
            for rule in self.rules:
                if self.updateKnowledge(rule):
                    updated = True
        pass

    def takeAction(self):
        pass

    def generateRoute(self):
        pass