def initializeBoard(board):
    count = 0

    for i in range (0, 3):
        row = []
        for j in range (0, 3):
            count += 1
            row.append(count)
        board.append(row)

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

    return "Continue"


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

def displayGameBoard(board):
    line0 = ' ' + str(board[0][2]) + ' | ' + str(board[1][2]) + ' | ' + str(board[2][2])
    line1 = '---+---+---'
    line2 = ' ' + str(board[0][1]) + ' | ' + str(board[1][1]) + ' | ' + str(board[2][1])
    line3 = '---+---+---'
    line4 = ' ' + str(board[0][0]) + ' | ' + str(board[1][0]) + ' | ' + str(board[2][0])

    print(line0)
    print(line1)
    print(line2)
    print(line3)
    print(line4)

def checkValidMove(board, intPosition):
    count = 0
    for i in range(0, 3):
        for j in range(0, 3):
            count +=1
            if count == intPosition:
                if board[i][j] != 'X' and board[i][j] != 'O':
                    return True

def assignMove(board, intPosition, player):
    count = 0
    for i in range(0, 3):
        for j in range(0, 3):
            count += 1
            if count == intPosition:
                board[i][j] = player
                print("player assigned")

def displayBanner():

    print("  _______         ______              ______ ")
    print(" /_  __(_)____   /_  __/___ ______   /_  __/___  ___ ")
    print("  / / / / ___/    / / / __ `/ ___/    / / / __ \/ _ \ ")
    print(" / / / / /__     / / / /_/ / /__     / / / /_/ /  __/ ")
    print("/_/ /_/\___/    /_/  \__,_/\___/    /_/  \____/\___/ ")
    print()

def is_valid(the_position):
    return the_position.isdigit() and 1 <= int(the_position) <= 9
    
def getPosition():
    position = input("Make a move (number between 1 and 9):  ")
    
    if is_valid(position):
        print("You selected " , position)
        return int(position)
    else:
        print("Invalid input.")
        getPosition()

def main():

    gameBoard = []
    player = 'X'

    initializeBoard(gameBoard)
    displayBanner()

    move = 0

    win = False

    while move < 9:
        move += 1

        displayGameBoard(gameBoard)

        valid = False

        while not valid:
            intPosition = getPosition()
            valid = checkValidMove(gameBoard, intPosition)
        
        assignMove(gameBoard, intPosition, player)

        c = checkGameOver(gameBoard)
        if c != "Continue":
            print("Player " + c + " wins!")
            win = True
            break

        if player == "X":
            player = 'O'
            
        else:
            player = "X"

    if not win:
        print("Tie")

main()