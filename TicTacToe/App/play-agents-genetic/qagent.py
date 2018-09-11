from player import *
from utils import load
import random
import threading
class QAgent(Player):
    def __init__(self, name):
        super().__init__(name)
        try:
            self.Memory = load()
        except:
            self.Memory = {}
        #print(self.Memory)
        self.CurrentMove = (-1,-1)
        self.lock = threading.Lock()

    def GetLeagalMoves(self, board):
        moves = []
        for i in range(0,3):
            for j in range(0,3):
                if board[i][j] != 'X' and board[i][j] != 'O':
                    moves.append((i,j))
        return moves

    def GetQValueOfMove(self, move, board):
        moves = self.Memory.get(self.bts(board), {})
        return moves.get(str(move),0)

    def bts(self, board):
        s = ""
        for i in range(0,3):
            for j in range(0,3):
                s+=str(board[i][j])
        return s

    def GetMove(self, board):
        random.seed()
        legalMoves = self.GetLeagalMoves(board)
        #print("All leagal moves: ", legalMoves)
        # always exploring, no policy yet
        # This is where the policy code would go
        # m = random.choice(legalMoves)
        m = random.choice(legalMoves)
        for c in legalMoves:
            if self.GetQValueOfMove(c,board) > self.GetQValueOfMove(m,board):
                # print("made best choice: ", c, self.GetQValueOfMove(c,board), " over: ", m, self.GetQValueOfMove(m,board) )
                m = c

        self.UpdateMemory(board,legalMoves)
        return m[0], m[1]
    
    def SendGameOverMessage(self, result, board):
        super().SendGameOverMessage(result,board)
        #self.Mutate(0)
        #print(self.Memory)

    def UpdateMemory(self, board, allmoves):
        with self.lock:
            if self.Memory.get(self.bts(board), False):
                return
            else:
                moves = {}
                for m in allmoves:
                    moves[str(m)] = 0
                self.Memory[self.bts(board)] = moves

    def Mutate(self, mutationRate):
        NewMemory = {}
        rewards = [-1,1,2]
        for board in self.Memory:
            moves = self.Memory.get(board, False)
            mutatedMoves = {}
            for m in moves:
                if mutationRate > random.uniform(0, 1):
                    mutatedMoves[m] = moves.get(m, False) + random.choice(rewards)
                else:
                    mutatedMoves[m] = moves.get(m,0)
            NewMemory[board] = mutatedMoves
        return NewMemory
            


        # try:
        #     self.Memory[state] = self.Memory[state] + self.Memory[nextstate]
        #     #print("\n\n\n\nupdated\n\n\n\n\n\n")
        #     #print(self.Memory)
        # except:
        #     self.Memory[nextstate] = 0.01
        #     #print("set 0")


