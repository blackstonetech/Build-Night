import json

def displayBanner():

    print("  _______         ______              ______ ")
    print(" /_  __(_)____   /_  __/___ ______   /_  __/___  ___ ")
    print("  / / / / ___/    / / / __ `/ ___/    / / / __ \/ _ \ ")
    print(" / / / / /__     / / / /_/ / /__     / / / /_/ /  __/ ")
    print("/_/ /_/\___/    /_/  \__,_/\___/    /_/  \____/\___/ ")
    print()

def checkGameOver(board):

    R = checkWinRows(board, "X")
    C = checkWinCols(board, "X")
    D = checkWinsDiagonal(board, "X")

    if R or C or D:
        return "X"

    R = checkWinRows(board, "O")
    C = checkWinCols(board, "O")
    D = checkWinsDiagonal(board, "O")

    if R or C or D:
        return "O"

    # check for tie
    for i in range(0,3):
        for j in range(0,3):
            if board[i][j] != 'X' and board[i][j] != 'O':
                return "Continue"
                
    return 'Tie'


def checkWinRows(board, player):
    for i in range(0,3):
        if board[i][0] == player and board[i][1] == player and board[i][2] == player:
            return True
    return False


def checkWinCols(board, player):
    for j in range(0,3):
        if board[0][j] == player and board[1][j] == player and board[2][j] == player:
            return True
    return False


def checkWinsDiagonal(board, player):
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True

    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True

    return False

def store(memDump, path="memDump.json"):
    dump = json.dumps(memDump)
    f = open(path, "w+")
    f.write(dump)
    f.close()

def storeOrig(memDump, path="origScore.json"):
    dump = json.dumps(memDump)
    f = open(path, "w+")
    f.write(dump)
    f.close()

def load(path="memDump.json"):
    f = open(path, "r")
    memDump = json.load(f)
    return memDump

def combine(source, overwrite):
    output = {}
    # for each key in source
    for key in source:
        # get the value in source
        s = source[key]
        # find the same key in overwrite
        o = overwrite.get(key,0)
        # if source == 0, substitute for the value in overwrite
        if (s == 0 and o != 0):
            output[key] = o
        # if source != 0 && overwrite != 0, average the two as floatsss
        elif (o != 0):
            output[key] = (o + s) / 2.0
        # otherwise take the original value
        else:
            output[key] = s
    return output
