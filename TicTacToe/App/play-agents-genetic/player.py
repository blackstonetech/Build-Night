class Player:
    def __init__(self, name):
        self.Name = name
        self.Wins = 0

    def GetMove(self, board):
        pass

    def SendGameOverMessage(self, result, board):
        if result == self.Name:
            self.Wins+=1

    def PlayAgain(self):
        return True