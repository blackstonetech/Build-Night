from manualagent import *
from randomagent import *
from game import *
from utils import *
import sys
# Take in cmd args
# Setup game
#   Choose agent to play the game
#   Init board class
# Should abstract (random, qlearning, and user input) into player class with common methods like
#       .GetMove()
# Game loop until game reaches conclusion
# Ask if users want to play again

displayBanner()

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
    elif sys.argv[1] == 'rr':
        game = Game(RandomAgent('X'),RandomAgent('O'))
        print("result: ", game.PlayGame())