from utils import *
from game import *
from qagent import *
import random, boto3, datetime
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
                score += 10
            elif result == "Tie":
                score-=1
            else:
                score-=5
        return score

    def RunGenerations(self, generations):
        try:
            #filePrefix = '/home/ec2-user/'
            self.Viz_data = load('VizData.json')
        except:
            self.Viz_data = {}
        dataPoint = {}
        bestscore = self.AssesFitness(RandomAgent('X'), self.Best, 10000)
        dataPoint['original-baseline'] = bestscore
        allgenerationdata = []
        for i in range(0, generations):
            scores = []
            # store(self.Best.Memory, "memDump_"+ str(bestScore) + ".json")
            agents = []
            generation = {}
            for a in range(0, self.Popsize):
                #make agents
                muteagent = QAgent('O')
                muteagent.Memory = self.Best.Mutate(self.mutationRate)
                agents.append(muteagent)

            for b in range(0, self.Popsize):
                score = self.AssesFitness(RandomAgent('X'), agents[b], 10000)
                scores.append(score)
                if score > bestscore:
                    bestscore = score
                    self.Best = agents[b]

            generation['scores'] = scores
            generation['most-fit'] = bestscore
            allgenerationdata.append(generation)
        dataPoint['generations'] = allgenerationdata
        dataPoint['new-baseline'] = bestscore
        # write data point
        self.Viz_data[str(datetime.datetime.now())] = dataPoint
        store(self.Viz_data,'VizData.json')
        try:
            s = boto3.client('sns', region_name='us-east-1')
            s.publish(Message='Current Score: ' + str(bestscore), PhoneNumber='+13015025813')
        except:
            print("Could not send text update")
        return self.Best
    

