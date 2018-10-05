from utils import *
from game import *
from qagent import *
import random, boto3, datetime
from randomagent import *

class Population():
    def __init__(self, size, fit, originalAgent):
        self.Best = originalAgent
        self.Popsize = size
        self.FitnessTest = fit

    def AssesFitness(self, agent1, agent2, trials):
        if agent1.Name == 'X' and agent2.Name == 'O':
            agentX = agent1
            agentO = agent2
        elif agent1.Name == 'O' and agent2.Name == 'X':
            agentX = agent2
            agentO = agent1
        else:
            print("Fitness assessment error")
            return 0
        score = 0
        for i in range(0,trials):
            game = Game(agentX,agentO)
            result = game.PlaySilentGame()
            if result == agent1.Name:
                score += 10
            elif result == "Tie":
                score-=1
            else:
                score-=5
        return score

    def RunGenerations(self, generations, opponent):

        # setup
        dataPoint = {}
        bestscore = 0
        allgenerationdata = []

        # load Historical Data
        try:
            self.Viz_data = load('VizData.json')
        except:
            self.Viz_data = {}

        # Training X or training O
        if self.Best.Name == 'O':
            bestscore = self.AssesFitness(self.Best, opponent, self.FitnessTest)
        elif self.Best.Name == 'X':
            bestscore = self.AssesFitness(self.Best, opponent, self.FitnessTest)
        else:
            print("Name of best not known")

        dataPoint['original-baseline'] = bestscore

        for i in range(0, generations):
            scores = []
            # store(self.Best.Memory, "memDump_"+ str(bestScore) + ".json")
            agents = []
            generation = {}
            for a in range(0, self.Popsize):
                #make agents
                muteagent = QAgent(self.Best.Name)
                muteagent.Memory = self.Best.Mutate()
                # print("Mutating to make new agent self.Best.Memory:", self.Best.Memory)
                agents.append(muteagent)
            #print(agents)
            for b in range(0, self.Popsize):
                score = self.AssesFitness(agents[b], opponent,  self.FitnessTest)
                scores.append(score)
                if score > bestscore:
                    bestscore = score
                    self.Best = agents[b]
            #print("Final selection of generation:",self.Best.Memory)
            generation['scores'] = scores
            generation['most-fit'] = bestscore
            allgenerationdata.append(generation)
        dataPoint['generations'] = allgenerationdata
        dataPoint['new-baseline'] = bestscore
        dataPoint['agent-name'] = self.Best.Name
        # write data point
        self.Viz_data[str(datetime.datetime.now())] = dataPoint
        store(self.Viz_data, 'VizData.json')
        try:
            s = boto3.client('sns', region_name='us-east-1')
            s.publish(Message='Current Score: ' + str(bestscore), PhoneNumber='+13015025813')
        except:
            print("Could not send text update")
        return self.Best
    

