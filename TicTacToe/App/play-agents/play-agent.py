from manualagent import *
from randomagent import *
from qagent import *
from game import *
from utils import *
import sys, threading
# Take in cmd args
# Setup game
#   Choose agent to play the game
#   Init board class
# Should abstract (random, qlearning, and user input) into player class with common methods like
#       .GetMove()
# Game loop until game reaches conclusion
# Ask if users want to play again

displayBanner()

class myThread (threading.Thread):
   def __init__(self, threadID, agentX, agentO):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.aX = agentX
        self.aO = agentO
   def run(self):
        #print ("Starting " + self.threadID)
        game = Game(self.aX,self.aO)
        game.PlaySilentGame()
        #print("Exiting " + self.threadID)

def PlayGameThread(agentX, agentO):
    game = Game(agentX,agentO)
    game.PlaySilentGame()

def PlayNGamesThreaded(N,agentX, agentO):
    t = []
    for i in range(0,N):
        t.append(myThread(str(i),agentX,agentO))
        # print(threading.activeCount())
    
    for i in range(0,N):
        t[i].start()

    for i in range(0,N):
        t[i].join()

    
    

def PlayNGames(N,agentX, agentO):
    for _ in range(0,N):
        game = Game(agentX,agentO)
        game.PlaySilentGame()
        #print("result: ", game.PlaySilentGame())

if len(sys.argv) == 1:
    game = Game(RandomAgent('X'),RandomAgent('O'))
    print("result: ", game.PlayGame())
else:
    if sys.argv[1] == 'mm':
        game = Game(ManualAgent('X'),ManualAgent('O'))
        print("result: ", game.PlayGame())
    elif sys.argv[1] == 'mr':
        game = Game(ManualAgent('X'),RandomAgent('O'))
        print("result: ", game.PlayGame())
    elif sys.argv[1] == 'mq':
        aX = RandomAgent('X')
        aO = QAgent('O')
        PlayNGamesThreaded(int(sys.argv[2]),aX,aO)
        print("aX wins:", aX.Wins)
        print("aO wins:", aO.Wins)
        #print("Mem:", aO.Memory)
        game = Game(ManualAgent('X'),aO)
        print("result: ", game.PlayGame())

    elif sys.argv[1] == 'qm':
        aX = QAgent('X')
        aO = RandomAgent('O')
        PlayNGamesThreaded(int(sys.argv[2]),aX,aO)
        print("aX wins:", aX.Wins)
        print("aO wins:", aO.Wins)
        #print("Mem:", aO.Memory)
        game = Game(aX,ManualAgent('O'))
        print("result: ", game.PlayGame())
        store(aX.Memory)

    elif sys.argv[1] == 'rq':
        aX = RandomAgent('X')
        aO = QAgent('O')
        PlayNGamesThreaded(int(sys.argv[2]),aX,aO)
        print("aX wins:", aX.Wins)
        print("aO wins:", aO.Wins)
        #print("Mem:", aO.Memory)
        game = Game(RandomAgent('X'),aO)
        print("result: ", game.PlayGame())
        store(aO.Memory)
        print("mem length:", len(aO.Memory))

    elif sys.argv[1] == 'qr':
        aX = QAgent('X')
        aO = RandomAgent('O')
        PlayNGamesThreaded(int(sys.argv[2]),aX,aO)
        print("aX wins:", aX.Wins)
        print("aO wins:", aO.Wins)
        #print("Mem:", aO.Memory)
        game = Game(RandomAgent('X'),aO)
        print("result: ", game.PlayGame())
        store(aX.Memory)
        print("mem length:", len(aX.Memory))

    elif sys.argv[1] == 'qq':
        aX = QAgent('X')
        aO = QAgent('O')
        PlayNGamesThreaded(int(sys.argv[2]),aX,aO)
        print("aX wins:", aX.Wins)
        print("aO wins:", aO.Wins)
        #print("Mem:", aO.Memory)
        game = Game(aX,aO)
        print("result: ", game.PlayGame())
        store(combine(aX.Memory, aO.Memory))
        print(len(combine(aX.Memory, aO.Memory)))

    elif sys.argv[1] == 'rr':
        aX = RandomAgent('X')
        aO = RandomAgent('O')
        PlayNGamesThreaded(int(sys.argv[2]),aX,aO)
        print("aX wins:", aX.Wins)
        print("aO wins:", aO.Wins)


