from WumpWorld import *

'''
Agent class, contains all the decision making, knowledge base, etc of the agent
'''

# class to hold simplified implication statements
class Implies:
    def __init__(self, LHS, RHS, type):
        self.LHS = LHS
        self.RHS = RHS
        self.type = type


class Agent:

    # initialize instance of agent
    def __init__(self, world):
        self.world = world
        self.arrows = 0
        self.wumpusAlive = 0
        self.frontierCells = 0
        self.safeCells = 0
        self.pathingRoute = 0
        self.knowledge = [world.size + 1][world.size + 1]
        self.pos = [0,0]
        self.up = [self.pos[0], self.pos[1] + 1]
        self.down = [self.pos[0], self.pos[1] - 1]
        self.left = [self.pos[0] - 1, self.pos[1]]
        self.up = [self.pos[0] + 1, self.pos[1]]
        self.direction = 0
        self.dead = False
        self.won = False
        self.rules = []
        self.populateRules()

    def initKnowledge(selfself):

    # populate rules [] with all the rules we are defining
    def populateRules(self):
        # if empty, all adjacent cells are safe
        self.rules.append(Implies("empty", "safe", "and"))
        # if stench, atleast one adjcaent cell has wumpus
        self.rules.append(Implies("stench", "wumpus", "or"))
        # if breeze, atleast one adjacent cell has pit
        self.rules.append(Implies("breeze", "pit", "or"))
        # if scream, wumpus has died
        self.rules.append(Implies("scream", "death", "facing"))
        # if bump, there is a wall where move was attempted
        self.rules.append(Implies("bump", "wall", "facing"))
        # mark a wall as safe, as it cannot be a wumpus or pit
        self.rules.append(Implies("wall", "safe", "is"))
        # if safe, not pit
        self.rules.append(Implies("safe", "pit", "not"))
        # if safe, not wumpus
        self.rules.append(Implies("safe", "wumpus", "not"))

    def updateKnowledge(self, x, y, term):
        if term not in self.knowledge[x][y]:
            self.knowledge[x][y].append(term)
            # if there is a change, check whether it changes anything else at position
            self.inferenceSystem(x, y, term)
            return True
        return False

    # update knowledge base based on a single rule
    def resolve(self, x, y, rule, percept):
        # if type is and, adjust all adjacent
        if rule.type == "and":
            if rule.LHS == percept:
                if (self.updateKnowledge(x, y + 1, rule.RHS) or
                self.updateKnowledge(x, y - 1, rule.RHS) or
                self.updateKnowledge(x - 1, y, rule.RHS) or
                self.updateKnowledge(x + 1, y, rule.RHS)):
                    return True
        # if type is or, check if only one is still possible
        if rule.type == "or":
            templist = []
            templist.append(self.knowledge[x][y + 1])
            templist.append(self.knowledge[x][y + 1])
            templist.append(self.knowledge[x][y + 1])
            templist.append(self.knowledge[x][y + 1])






    # iterate through all the rules and update each one until nothing else can be updated with new knowledge
    def inferenceSystem(self, x, y, percept):
        updated = True
        while updated:
            updated = False
            for rule in self.rules:
                if self.resolve(rule, x, y, percept):
                    updated = True

    def takeAction(self):
        #check percepts in current spot
        percept = self.world.perceiveCell(self.pos[0], self.pos[1])
        # check for game ending conditions
        if 'glitter' in percept:
            self.won == True
            return "Won"
        if 'wumpus' in percept or 'pit' in percept:
            self.dead == True
            return "Dead"
        #run inference system to update knowledge base
        self.inferenceSystem(self.pos[0], self.pos[1], percept)
        pass

    def generateRoute(self):
        pass
