from utils import *
from game import *
from qagent import *
import random
from randomagent import *

class Population():
    def __init__(self, size, mutationRate, originalAgent):
        self.Best = originalAgent
        self.Popsize = size
        self.mutationRate = mutationRate

    def AssesFitness(self, agentX, agentO, trials):
        score = 0
        for i in range(0,trials):
            game = Game(agentX,agentO)
            result = game.PlaySilentGame()
            if result == agentO.Name:
                score += 2
            elif result == "Tie":
                score+=1
            else:
                score-=1
        return score

    def RunGenerations(self, generations):
        bestScore = self.AssesFitness(RandomAgent('X'), self.Best, 10000)
        print("before score", bestScore)
        for i in range(0,generations):
            if i%100 == 0:
                store(self.Best.Memory, "memDump_"+ str(bestScore) + ".json")
            for a in range(0,self.Popsize):
                muteagent = QAgent('O')
                score = self.AssesFitness(RandomAgent('X'), muteagent, 10000)
                muteagent.Memory = self.Best.Mutate(self.mutationRate)
                if  score > bestScore:
                    bestScore = score
                    self.Best = muteagent
        print("after score", bestScore)
        return self.Best
    

