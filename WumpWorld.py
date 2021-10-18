"""
Game state manager and world generator
"""

import random
import copy

class WumpWorld:
    def __init__(self, size, P_pit, P_obs, P_wumpus):
        self.sqSize = size
        self.P_pit = P_pit
        self.P_obs = P_obs
        self.P_wumpus = P_wumpus
        self.board = [size][size]

    # problem/world generator function
    def generateProblem(self):
        startX, startY = [random.randint(0, self.sqSize-1), random.randint(0, self.sqSize-1)]
        self.board[startX][startY] = 'empty'
        goldX, goldY = [startX, startY]
        while [goldX, goldY] == [startX, startY]:
            goldX, goldY = [random.randint(0, self.sqSize-1), random.randint(0, self.sqSize-1)]
        self.board[goldX, goldY] = 'gold'
        for x in range(self.sqSize):
            for y in range(self.sqSize):
                # make sure not to override the agent's start space or the gold
                if([x,y] != [startX,startY] and [x,y] != [goldX,goldY]):
                    rand = random.random
                    if(rand < self.P_pit):
                        self.board[x][y] = 'pit'
                    elif(rand < (self.P_pit + self.P_obs)):
                        self.board[x][y] = 'wall'
                    elif (rand < (self.P_pit + self.P_obs + self.P_wumpus)):
                        self.board[x][y] = 'wumpus'
                    else:
                        self.board[x][y] = 'empty'
        # return the starting position so the agent knows where it is
        return startX, startY

    # make a duplicate world for controlled experiments
    def duplicateProblem(self, otherWorld):
        return copy.deepcopy(otherWorld)

    # print out the current board state
    def printWorld(self):
        pass

    def validCell(self, x, y):
        if(x < 0 or y < 0):
            return False
        elif(x > self.sqSize-1 or y > self.sqSize-1):
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

        #Assume agent hit a wall if cell is not valid
        if( (not self.validCell(x,y)) or (self.board[x][y] == 'wall') ):
            return ['bump']

        # start with an empty list; everything perceived will be added to it
        perception = []
        # list adjacent cells
        up = [x,y-1]
        down = [x,y+1]
        left = [x-1,y]
        right = [x+1,y]

        # check for gold on actual cell
        if(self.board[x][y] == 'gold'):
            perception.append('glitter')

        # listing things sensed in adjacent cells
        for j,k in [up,down,left,right]:
            if(self.validCell(j,k)):
                if(self.board[j,k] == 'wumpus'):
                    perception.append('stench')
                elif(self.board[j,k] == 'pit'):
                    perception.append('breeze')

        # check for empty list, label as empty if so
        if not perception:
            perception.append('empty')

        return perception