from WumpWorld import *
import random

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
    def __init__(self, world, x, y, arrows):
        self.actions = 0
        self.world = world
        self.arrows = arrows
        self.wumpusDead = 0
        self.frontierCells = set([])
        self.safeCells = set([])
        self.pathingRoute = []
        self.knowledge = [world.size + 2][world.size + 2]  # add buffer around world for safe markers
        self.pos = [x, y]
        self.direction = 0  # like unit circle, 0 is facing right, 90 up, 180 left, 270 down
        self.deadbyWumpus = False
        self.deadbyPit = False
        self.won = False
        self.rules = []
        self.populateRules()

    # populate the initial knowledge base
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
            if rule.LHS == percept:
                templist = [self.knowledge(x, y - 1), self.knowledge(x, y + 1), self.knowledge(x - 1, y),
                            self.knowledge(x + 1, y)]
                if templist.count("safe") == 3:
                    if "safe" not in (self.knowledge(x, y - 1)):
                        (self.knowledge(x, y - 1)).append(rule.RHS)
                        updated = True
                    if "safe" not in (self.knowledge(x, y + 1)):
                        (self.knowledge(x, y + 1)).append(rule.RHS)
                        updated = True
                    if "safe" not in (self.knowledge(x - 1, y)):
                        (self.knowledge(x - 1, y)).append(rule.RHS)
                        updated = True
                    if "safe" not in (self.knowledge(x + 1, y)):
                        (self.knowledge(x + 1, y)).append(rule.RHS)
                        updated = True
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
                    if self.updateKnowledge(x, y - 1, rule.RHS):
                        updated = True
        # if type is is, just check current tile
        if rule.type == "is":
            if rule.LHS == percept:
                if self.updateKnowledge(x, y, rule.RHS):
                    updated = True
        return updated

    # iterate through all the rules and update each one until nothing else can be updated with new knowledge
    def inferenceSystem(self, x, y, percept):
        updated = True
        while updated:
            updated = False
            for rule in self.rules:
                if self.resolve(rule, x, y, percept):
                    updated = True

    def takeAction(self, bumped):
        x = self.pos[0]
        y = self.pos[1]
        self.actions += 1
        # check percepts in current spot
        percept = self.world.perceiveCell(self.pos[0], self.pos[1])
        # check for game ending conditions
        if 'glitter' in percept:
            self.won == True
            return "Won"
        if 'wumpus' in percept:
            self.deadbyWumpus == True
            return "Wumpus"
        if 'pit' in percept:
            self.deadbyPit == True
            return "Pit"

        # if was bumped previous time, add bump to percepts so its properly processed this time
        if bumped:
            percept.append("bump")

        bumped = False
        popped = False
        # run inference system to update knowledge base
        self.inferenceSystem(self.pos[0], self.pos[1], percept)
        # add new cells to safelist and frontier list
        # we know its safe since we are currently here!
        self.safeCells.append((self.pos[0], self.pos[1]))

        # add to frontierlist, but only if stil unexplored, safe, and not a wall
        if ("safe" in self.knowledge[self.pos[0]][self.pos[1] + 1]) and (
                (self.pos[0], self.pos[1] + 1) not in self.safeCells) and "wall" not in self.knowledge[self.pos[0]][
            self.pos[1] + 1]:
            self.frontierCells.append((self.pos[0], self.pos[1] + 1))
        if ("safe" in self.knowledge[self.pos[0]][self.pos[1] - 1]) and (
                (self.pos[0], self.pos[1] - 1) not in self.safeCells) and "wall" not in self.knowledge[self.pos[0]][
            self.pos[1] - 1]:
            self.frontierCells.append((self.pos[0], self.pos[1] - 1))
        if ("safe" in self.knowledge[self.pos[0] - 1][self.pos[1]]) and (
                (self.pos[0] - 1, self.pos[1]) not in self.safeCells) and "wall" not in self.knowledge[self.pos[0] - 1][
            self.pos[1]]:
            self.frontierCells.append((self.pos[0] - 1, self.pos[1]))
        if ("safe" in self.knowledge[self.pos[0] + 1][self.pos[1]]) and (
                (self.pos[0] + 1, self.pos[1]) not in self.safeCells) and "wall" not in self.knowledge[self.pos[0] + 1][
            self.pos[1]]:
            self.frontierCells.append((self.pos[0] + 1, self.pos[1]))

        # first, if known next to wumpus, kill it, then try moving otherwise
        # by default, if multiple safe adjacent options will choose to go right first then ccw for choosing
        # if its a wall, note there is a bump there which will be carried into next call
        if "wumpus" in self.knowledge[self.pos[0] + 1][self.pos[1]]:
            if self.world.board[self.pos[0] + 1][self.pos[1]] == "wumpus":
                self.wumpusDead += 1
                self.arrows -= 1
                self.world.board[self.pos[0] + 1][self.pos[1]] = "empty"
                self.knowledge[self.pos[0] + 1][self.pos[1]].remove("wumpus")
            else:
                self.arrows -= 1
                self.knowledge[self.pos[0] + 1][self.pos[1]].remove("wumpus")
        elif "wumpus" in self.knowledge[self.pos[0]][self.pos[1] + 1]:
            if self.world.board[self.pos[0]][self.pos[1] + 1] == "wumpus":
                self.wumpusDead += 1
                self.arrows -= 1
                self.world.board[self.pos[0]][self.pos[1] + 1] = "empty"
                self.knowledge[self.pos[0]][self.pos[1] + 1].remove("wumpus")
            else:
                self.arrows -= 1
                self.knowledge[self.pos[0]][self.pos[1] + 1].remove("wumpus")
        elif "wumpus" in self.knowledge[self.pos[0] - 1][self.pos[1]]:
            if self.world.board[self.pos[0] - 1][self.pos[1]] == "wumpus":
                self.wumpusDead += 1
                self.arrows -= 1
                self.world.board[self.pos[0] - 1][self.pos[1]] = "empty"
                self.knowledge[self.pos[0] - 1][self.pos[1]].remove("wumpus")
            else:
                self.arrows -= 1
                self.knowledge[self.pos[0]][self.pos[1] + 1].remove("wumpus")
        elif "wumpus" in self.knowledge[self.pos[0]][self.pos[1] - 1]:
            if self.world.board[self.pos[0]][self.pos[1] - 1] == "wumpus":
                self.wumpusDead += 1
                self.arrows -= 1
                self.world.board[self.pos[0]][self.pos[1] - 1] = "empty"
                self.knowledge[self.pos[0]][self.pos[1] - 1].remove("wumpus")
            else:
                self.arrows -= 1
                self.knowledge[self.pos[0]][self.pos[1] - 1].remove("wumpus")
        elif (self.pos[0] + 1, self.pos[1]) in self.frontierCells:
            self.direction = 0
            if "bump" not in self.world.perceiveCell(self.pos[0] + 1, self.pos[1]):
                self.pos[0] += 1
            else:
                self.frontierCells.remove((self.pos[0] + 1, self.pos[1]))
                bumped = True
        elif (self.pos[0], self.pos[1] + 1) in self.frontierCells:
            self.direction = 90
            if "bump" not in self.world.perceiveCell(self.pos[0], self.pos[1] + 1):
                self.pos[1] += 1
            else:
                self.frontierCells.remove((self.pos[0], self.pos[1] + 1))
                bumped = True
        elif (self.pos[0] - 1, self.pos[1]) in self.frontierCells:
            self.direction = 180
            if "bump" not in self.world.perceiveCell(self.pos[0] - 1, self.pos[1]):
                self.pos[0] -= 1
            else:
                self.frontierCells.remove((self.pos[0] - 1, self.pos[1]))
                bumped = True
        elif (self.pos[0], self.pos[1] - 1) in self.frontierCells:
            self.direction = 270
            if "bump" not in self.world.perceiveCell[self.pos[0]][self.pos[1] - 1]:
                self.pos[1] -= 1
            else:
                self.frontierCells.remove((self.pos[0], self.pos[1] - 1))
                bumped = True
        elif self.pathingRoute:  # start backtracking if pathingRoute is not empty
            newspot = self.pathingRoute.pop()
            self.pos[0] = newspot[0]
            self.pos[1] = newspot[1]
            popped = True
        else:  # if all else fails, just go to a random adjacent cell or shoot random adjacent cell
            self.direction = random.randint(0, 3) * 90
            if self.direction == 0:
                self.pos[0] += 1
            elif self.direction == 90:
                self.pos[1] += 1
            elif self.direction == 180:
                self.pos[0] -= 1
            elif self.direction == 270:
                self.pos[1] -= 1
        # before moving on, add current cell to pathing route stack if any position has changed and not already backtracking
        if (x != self.pos[0] or y != self.pos[1]) and not popped:
            self.pathingRoute.append((self.pos[0], self.pos[1]))

        return bumped

    def solve(self):
        bumped = False
        while not (self.won or self.deadbyWumpus or self.deadbyPit):
            bumped = self.takeAction(bumped)

        # returns if gold found or dead, number of wumpus killed, number of cells explored, and number of actions
        return self.won, self.dead, self.wumpusDead, len(self.safeCells), self.actions
