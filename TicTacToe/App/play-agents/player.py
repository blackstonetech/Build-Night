class Player:
    def __init__(self, name):
        self.Name = name

    def GetMove(self, board):
        pass

    def SendGameOverMessage(self, result):
        pass

    def PlayAgain(self):
        return True