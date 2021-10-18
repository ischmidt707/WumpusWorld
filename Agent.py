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
        self.frontierCells = set([])
        self.safeCells = set([])
        self.pathingRoute = 0
        self.knowledge = [world.size + 2][world.size + 2] # add buffer around world for safe markers
        self.pos = [1,1]
        self.direction = 0 # like unit circle, 0 is facing right, 90 up, 180 left, 270 down
        self.dead = False
        self.won = False
        self.rules = []
        self.populateRules()

    #populate the initial knowledge base
    def initKnowledge(self):
        pass
    # populate rules [] with all the rules we are defining
    def populateRules(self):
        # if empty, all adjacent cells are safe
        self.rules.append(Implies("empty", "safe", "and"))
        # if stench, atleast one adjcaent cell has wumpus
        self.rules.append(Implies("stench", "wumpus", "or"))
        # if breeze, atleast one adjacent cell has pit
        self.rules.append(Implies("breeze", "pit", "or"))
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
        updated = False
        # if type is and, adjust all adjacent
        if rule.type == "and":
            if rule.LHS == percept:
                if (self.updateKnowledge(x, y + 1, rule.RHS) or
                    self.updateKnowledge(x, y - 1, rule.RHS) or
                    self.updateKnowledge(x - 1, y, rule.RHS) or
                    self.updateKnowledge(x + 1, y, rule.RHS) or
                    self.updateKnowledge(x, y, rule.RHS)):
                    updated = True
        # if type is or, check if only one is still possible
        if rule.type == "or":
            pass
        # if type is facing apply it only to tile agent is facing
        if rule.type == "facing":
            if rule.LHS == percept:
                if self.direction == 0:
                    if self.updateKnowledge(x + 1, y, rule.RHS):
                        updated = True
                if self.direction == 90:
                    if self.updateKnowledge(x, y + 1, rule.RHS):
                        updated = True
                if self.direction == 180:
                    if self.updateKnowledge(x - 1, y, rule.RHS):
                        updated = True
                if self.direction == 270:
                    if self.updateKnowledge(x, y-1, rule.RHS):
                        updated = True
        #if type is is, just check current tile
        if rule.type == "is":
            if rule.LHS == percept:
                if self.updateKnowledge(x, y, rule.RHS):
                    updated = True
        #if
        if rule.type == "not":
            pass

        return updated

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
        #add new cells to safelist and frontier list
        # we know its safe since we are currently here!
        self.safeCells.append((self.pos[0], self.pos[1]))

        #add to frontierlist, but only if stil unexplored, safe, and not a wall
        if ("safe" in self.knowledge[self.pos[0]][self.pos[1] + 1]) and ((self.pos[0], self.pos[1] + 1) not in self.safeCells) and "wall" not in self.knowledge[self.pos[0]][self.pos[1] + 1]:
            self.frontierCells.append((self.pos[0], self.pos[1] + 1))
        if ("safe" in self.knowledge[self.pos[0]][self.pos[1] - 1]) and ((self.pos[0], self.pos[1] - 1) not in self.safeCells) and "wall" not in self.knowledge[self.pos[0]][self.pos[1] - 1]:
            self.frontierCells.append((self.pos[0], self.pos[1] - 1))
        if ("safe" in self.knowledge[self.pos[0] - 1][self.pos[1]]) and ((self.pos[0] - 1, self.pos[1]) not in self.safeCells) and "wall" not in self.knowledge[self.pos[0] - 1][self.pos[1]]:
            self.frontierCells.append((self.pos[0] - 1, self.pos[1]))
        if ("safe" in self.knowledge[self.pos[0] + 1][self.pos[1]]) and ((self.pos[0] + 1, self.pos[1]) not in self.safeCells) and "wall" not in self.knowledge[self.pos[0] + 1][self.pos[1]]:
            self.frontierCells.append((self.pos[0] + 1, self.pos[1]))

        #by default, if multiple safe adjacent options will choose to go up first then
        pass

    def solve(self):
        while not (self.won or self.dead):
            self.takeAction()
        if self.won:
            return "Won!"
        if self.dead:
            return "Dead"
    def generateRoute(self):
        pass
