from utils import checkGameOver

class Game:
    def __init__(self, agentX, agentO):
        self.AgentX = agentX
        self.AgentO = agentO
        self.initializeBoard()

    def initializeBoard(self):
        board = []
        count = 0

        for _ in range (0, 3):
            row = []
            for _ in range (0, 3):
                count += 1
                row.append(count)
            board.append(row)

        self.Board = board

    def PlayGame(self):
        self.DisplayBoard()
        result = self.CheckGameOver()
        currentPlayer = self.AgentX
        while result == 'Continue':
            x,y = currentPlayer.GetMove(self.Board)
            # check valid move
            while self.CheckValid(x,y) != True:
                x,y = currentPlayer.GetMove(self.Board)

            self.Board[x][y] = currentPlayer.Name
            currentPlayer = self.AgentO if currentPlayer == self.AgentX else self.AgentX
            result = self.CheckGameOver()
            self.DisplayBoard()

        return result

    def CheckGameOver(self):
        #from utils
        return checkGameOver(self.Board)

    def DisplayBoard(self):
        line0 = ' ' + str(self.Board[0][0]) + ' | ' + str(self.Board[0][1]) + ' | ' + str(self.Board[0][2])
        line1 = '---+---+---'
        line2 = ' ' + str(self.Board[1][0]) + ' | ' + str(self.Board[1][1]) + ' | ' + str(self.Board[1][2])
        line3 = '---+---+---'
        line4 = ' ' + str(self.Board[2][0]) + ' | ' + str(self.Board[2][1]) + ' | ' + str(self.Board[2][2])

        print(line0)
        print(line1)
        print(line2)
        print(line3)
        print(line4,'\n')
    
    def CheckValid(self,x,y):
        if self.Board[x][y] != 'X' and self.Board[x][y] != 'O':
            return True
        return False