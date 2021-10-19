"""
Game state manager and world generator
"""

import random
import copy


class WumpWorld:
    def __init__(self, size, P_pit, P_obs, P_wumpus):
        self.size = size
        self.P_pit = P_pit
        self.P_obs = P_obs
        self.P_wumpus = P_wumpus
        self.board = [[0 for i in range(size+2)] for j in range(size+2)]

    # problem/world generator function
    def generateProblem(self):

        # create walls around the border
        for j in range(self.size + 2):
            self.board[j][0] = 'wall'
            self.board[j][self.size + 1] = 'wall'
        for k in range(1, self.size + 1):
            self.board[0][k] = 'wall'
            self.board[self.size + 1][k] = 'wall'

        # we will keep track of how many wumpuses spawn so we have that many arrows
        wumpCount = 0

        # fill out the board randomly
        for y in range(1, self.size + 1):
            for x in range(1, self.size + 1):
                rand = random.random()
                if (rand < self.P_pit):
                    self.board[x][y] = 'pit'
                elif (rand < (self.P_pit + self.P_obs)):
                    self.board[x][y] = 'wall'
                elif (rand < (self.P_pit + self.P_obs + self.P_wumpus)):
                    self.board[x][y] = 'wumpus'
                    wumpCount += 1
                else:
                    self.board[x][y] = 'empty'

        # set start cell and gold at the end so they aren't overwritten
        startX, startY = [random.randint(1, self.size), random.randint(1, self.size)]
        self.board[startX][startY] = 'empty'
        goldX, goldY = [startX, startY]
        while [goldX, goldY] == [startX, startY]:
            goldX, goldY = [random.randint(1, self.size), random.randint(1, self.size)]
        self.board[goldX][goldY] = 'gold'

        # return the starting position so the agent knows where it is, and number of wumpuses
        return startX, startY, wumpCount

    # make a duplicate world for controlled experiments
    def duplicateProblem(self):
        return copy.deepcopy(self)

    # print out the current board state
    def printWorld(self):

        printDict = {
            "empty": "*",
            "pit": "P",
            "wumpus": "W",
            "wall": "O",
            "gold": "G",
            0: "#"# for debugging purposes when constructing the map
        }

        for y in range(self.size+2):
            for x in range(self.size+2):
                print(printDict[self.board[x][y]], end="")
            print("")
        print("")

    def validCell(self, x, y):
        if (x < 0 or y < 0):
            return False
        elif (x > self.size - 1 or y > self.size - 1):
            return False
        else:
            return True

    # return whatever is perceived in a requested cell
    def perceiveCell(self, x, y):
        """
        possible percepts:
        'stench' - wumpus is adjacent
        'breeze' - pit is adjacent
        'empty' - nothing perceived in this cell
        'bump' - hit a wall (calling function should not move the agent)
        'glitter' - gold in cell
        """

        # Assume agent hit a wall if cell is not valid
        if ((not self.validCell(x, y)) or (self.board[x][y] == 'wall')):
            return ['bump']

        # start with an empty list; everything perceived will be added to it
        perception = []
        # list adjacent cells
        up = [x, y - 1]
        down = [x, y + 1]
        left = [x - 1, y]
        right = [x + 1, y]

        # check for gold on actual cell
        if (self.board[x][y] == 'gold'):
            perception.append('glitter')

        # listing things sensed in adjacent cells
        for j, k in [up, down, left, right]:
            if (self.validCell(j, k)):
                if (self.board[j, k] == 'wumpus'):
                    perception.append('stench')
                elif (self.board[j, k] == 'pit'):
                    perception.append('breeze')

        # check for empty list, label as empty if so
        if not perception:
            perception.append('empty')

        return perception
