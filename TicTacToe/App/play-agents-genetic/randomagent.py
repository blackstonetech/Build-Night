import random

from player import *



class RandomAgent(Player):
    #let super handle __init__

    # Overide .GetMove(self, board)
    def GetMove(self, board):
        random.seed()
        while True:
            x = random.randint(0,2)
            y = random.randint(0,2)
            if board[x][y] != 'X' and board[x][y] != 'O':
                return x, y

    def PlayAgain(self):
        return True