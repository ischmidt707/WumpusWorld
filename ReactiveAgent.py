from WumpWorld import *
import random

"""
This is an alternative agent that uses less information than regular Agent.
It will be used as a control for comparisons.
"""


class ReactiveAgent:

    def __init__(self, world, x, y, arrows):
        self.world = world
        self.pos = [x,y]
        self.arrows = arrows
        self.actions = 0
        self.safelist = set([])
        self.frontierCells = set([])
        self.pathingRoute = []
        self.won = False
        self.deadbyWumpus = False
        self.deadbyPit = False
        self.direction = 0

    def takeAction(self):
        x = self.pos[0]
        y = self.pos[1]
        popped = False
        self.actions += 1
        percept = self.world.perceiveCell(x, y)
        if 'glitter' in percept:
            self.won = True
            return
        if 'wumpus' in percept:
            self.deadbyWumpus = True
            return
        if 'pit' in percept:
            self.deadbyPit = True
            return
        #current spot is confirmed to be safe and explored
        self.safelist.add((x,y))

        if "empty" in percept:
            self.frontierCells.add((self.pos[0] + 1, self.pos[1]))
            self.frontierCells.add((self.pos[0], self.pos[1] + 1))
            self.frontierCells.add((self.pos[0] - 1, self.pos[1]))
            self.frontierCells.add((self.pos[0], self.pos[1] - 1))

        if (self.pos[0] + 1, self.pos[1]) in self.frontierCells:
            self.direction = 0
            if "bump" not in self.world.perceiveCell(self.pos[0] + 1, self.pos[1]):
                self.pos[0] += 1
            else:
                self.frontierCells.remove((self.pos[0] + 1, self.pos[1]))
        elif (self.pos[0], self.pos[1] + 1) in self.frontierCells:
            self.direction = 90
            if "bump" not in self.world.perceiveCell(self.pos[0], self.pos[1] + 1):
                self.pos[1] += 1
            else:
                self.frontierCells.remove((self.pos[0], self.pos[1] + 1))
        elif (self.pos[0] - 1, self.pos[1]) in self.frontierCells:
            self.direction = 180
            if "bump" not in self.world.perceiveCell(self.pos[0] - 1, self.pos[1]):
                self.pos[0] -= 1
            else:
                self.frontierCells.remove((self.pos[0] - 1, self.pos[1]))
        elif (self.pos[0], self.pos[1] - 1) in self.frontierCells:
            self.direction = 270
            if "bump" not in self.world.perceiveCell[self.pos[0]][self.pos[1] - 1]:
                self.pos[1] -= 1
            else:
                self.frontierCells.remove((self.pos[0], self.pos[1] - 1))
        elif self.pathingRoute:  # start backtracking if pathingRoute is not empty
            newspot = self.pathingRoute.pop()
            self.pos[0] = newspot[0]
            self.pos[1] = newspot[1]
            popped = True
        else:  # if all else fails, just go to a random adjacent cell or shoot random adjacent cell
            self.direction = random.randint(0, 3) * 90
            if self.direction == 0:
                if self.world.board[self.pos[0] + 1][self.pos[1]] != "wall":
                    self.pos[0] += 1
            elif self.direction == 90:
                if self.world.board[self.pos[0]][self.pos[1] + 1] != "wall":
                    self.pos[1] += 1
            elif self.direction == 180:
                if self.world.board[self.pos[0] - 1][self.pos[1]] != "wall":
                    self.pos[0] -= 1
            elif self.direction == 270:
                if self.world.board[self.pos[0]][self.pos[1] - 1] != "wall":
                    self.pos[1] -= 1
            popped = True
        # before moving on, add current cell to pathing route stack if any position has changed and not already backtracking
        if (x != self.pos[0] or y != self.pos[1]) and not popped:
            self.pathingRoute.append((self.pos[0], self.pos[1]))

        return

    def solve(self):
        while not (self.won or self.deadbyWumpus or self.deadbyPit):
            self.takeAction()

        # returns if gold found or dead, number of wumpus killed, number of cells explored, and number of actions
        return self.won, self.deadbyWumpus, self.deadbyPit, len(self.safelist), self.actions
