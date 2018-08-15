from player import *

converter = {
    "1":(0,0),
    "2":(0,1),
    "3":(0,2),
    "4":(1,0),
    "5":(1,1),
    "6":(1,2),
    "7":(2,0),
    "8":(2,1),
    "9":(2,2)
}

class ManualAgent(Player):
    def __init__(self, name):
        self.Name = name

    def GetMove(self, board):
        return converter.get(input('Make a move (number between 1 and 9):  '))


    def SendGameOverMessage(self, result):
        if result == 'X' or result == 'O':
            print("Player " + result + " wins!")
        else:
            print('The game ended in a draw')
    
    def PlayAgain(self):
            return (True if input('Play Again? (y or n): ') == 'y' else False)