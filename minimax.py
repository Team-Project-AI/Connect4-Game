import numpy as np
import random
import pygame
import sys
import math

BLUE = (26, 26, 255)
WHITE = (244, 240, 224)
RED = (213, 46, 48)
YELLOW = (252, 238, 33)
BLACK = (0,0,0)
LIGHT_BLUE = (0, 0, 179)

NRows = 6
NColumns = 7
Limit = NColumns // 2

Computer = 0
Agent = 1

EMPTY = 0
CPiece = 1
APiece = 2

Connect = 4
Max = 100000000000000
Min = -100000000000000

level_depths = {"Easy": 2, "Medium": 3, "Hard": 4}
def createBoard():
    board = np.zeros((NRows, NColumns))
    return board


def dropPiece(board, row, col, piece):
    board[row][col] = piece


def isValidLocation(board, col):
    return board[NRows - 1][col] == 0


def getChildren(board, col):
    for row in range(NRows):
        if board[row][col] == 0:
            return row

def printBoard(board):
    print(np.flip(board,0))


def winning(board, piece):
    # Check horizontal locations for winer
    for col in range(NColumns - Limit):
        for row in range(NRows):
            if board[row][col] == piece and board[row][col + 1] == piece and board[row][col + 2] == piece and board[row][
                col + Limit] == piece:
                return True

    # Check vertical locations for winer
    for col in range(NColumns):
        for row in range(NRows - Limit):
            if board[row][col] == piece and board[row + 1][col] == piece and board[row + 2][col] == piece and board[row + Limit][
                col] == piece:
                return True

    # Check right diaganols
    for col in range(NColumns - Limit):
        for row in range(NRows - Limit):
            if board[row][col] == piece and board[row + 1][col + 1] == piece and board[row + 2][col + 2] == piece and board[row + Limit][
                col + Limit] == piece:
                return True

    # Check left diaganols
    for col in range(NColumns - Limit):
        for row in range(Limit, NRows):
            if board[row][col] == piece and board[row - 1][col + 1] == piece and board[row - 2][col + 2] == piece and board[row - Limit][
                col + Limit] == piece:
                return True


def calcScore(window, piece):
    score = 0
    opponent = CPiece
    if piece == CPiece:
        opponent = APiece

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2
    if window.count(opponent) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score


def state(board, piece):
    score = 0
    # Score center column
    centerArr = [int(i) for i in list(board[:, Limit])]
    centerCount = centerArr.count(piece)
    score += centerCount * 3

    # Score Horizontal
    for row in range(NRows):
        rowArr = [int(i) for i in list(board[row, :])]
        for col in range(NColumns - Limit):
            window = rowArr[col:col + Connect]
            score += calcScore(window, piece)

    # Score Vertical
    for col in range(NColumns):
        colArr = [int(i) for i in list(board[:, col])]
        for row in range(NRows - Limit):
            window = colArr[row:row + Connect]
            score += calcScore(window, piece)

    # Score right diagonal
    for row in range(NRows - Limit):
        for col in range(NColumns - Limit):
            window = [board[row + i][col + i] for i in range(Connect)]
            score += calcScore(window, piece)

    # Score left diagonal
    for row in range(NRows - Limit):
        for col in range(NColumns - Limit):
            window = [board[row + Limit - i][col + i] for i in range(Connect)]
            score += calcScore(window, piece)

    return score


def isTerminalNode(board):
    if len(getValidLocations(board)) == 0 or winning(board, CPiece) or winning(board, APiece):
        return True
    return False


def minimax(board, depth, maximizingPlayer):
    isTerminal = isTerminalNode(board)
    validLocations = getValidLocations(board)
    if depth == 0 or isTerminal:
        if isTerminal:
            if winning(board, APiece):
                return (Max, None)
            elif winning(board, CPiece):
                return (Min, None)
            else:  # Game is over, no more valid moves
                return (0, None)
        else:  # Depth is zero
            return (state(board, APiece), None)
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(validLocations)
        for col in validLocations:
            row = getChildren(board, col)
            bCopy = board.copy()
            dropPiece(bCopy, row, col, APiece)
            new_score = minimax(bCopy, depth - 1, False)[0]
            if new_score > value:
                value = new_score
                column = col
        return value, column

    else:  # Minimizing player
        value = math.inf
        column = random.choice(validLocations)
        for col in validLocations:
            row = getChildren(board, col)
            bCopy = board.copy()
            dropPiece(bCopy, row, col, CPiece)
            new_score = minimax(bCopy, depth - 1, True)[0]
            if new_score < value:
                value = new_score
                column = col
        return value, column

def getValidLocations(board):
    valid_locations = []
    for col in range(NColumns):
        if isValidLocation(board, col):
            valid_locations.append(col)
    return valid_locations

# select best move
def bestMove(board, piece):
    validLocations = getValidLocations(board)
    bestScore = -10000
    bestCol = random.choice(validLocations)
    for col in validLocations:
        row = getChildren(board, col)
        TBoard = board.copy()
        dropPiece(TBoard, row, col, piece)
        score = state(TBoard, piece)
        if score > bestScore:
            bestScore = score
            bestCol = col
    return bestCol

def drawBoard(board):
    for col in range(NColumns):
        for row in range(NRows):
            pygame.draw.rect(screen, YELLOW, (LeftMargin + col * BoardSize, TopMargin + row * BoardSize + BoardSize, BoardSize, BoardSize))
            pygame.draw.circle(screen, WHITE, (
                int(LeftMargin + col * BoardSize + BoardSize / 2), int(TopMargin + row * BoardSize + BoardSize + BoardSize / 2)), Radius)

    for col in range(NColumns):
        for row in range(NRows):
            if board[row][col] == CPiece:
                pygame.draw.circle(screen, RED, (
                    int(LeftMargin + col * BoardSize + BoardSize / 2), Height - int(TopMargin + row * BoardSize + BoardSize / 2)), Radius)
            elif board[row][col] == APiece:
                pygame.draw.circle(screen, BLUE, (
                    int(LeftMargin + col * BoardSize + BoardSize / 2), Height - int(TopMargin + row * BoardSize + BoardSize / 2)), Radius)
    pygame.display.update()

def displayMenu():
    global choice, d
    menuFont = pygame.font.SysFont("Open Sans", 50)
    title = menuFont.render("Connect Four Game", 1, BLUE)
    screen.blit(title, (Width / 2 - title.get_width() / 2, 50))

    # Define button dimensions
    buttonWidth = 200
    buttonHeight = 50

    # Create Easy button
    easyButtonRect = pygame.Rect((Width - buttonWidth) / 2, 200, buttonWidth, buttonHeight)
    easyButtonColor = BLUE
    pygame.draw.rect(screen, easyButtonColor, easyButtonRect)
    easy = menuFont.render("Easy", 1, WHITE)
    screen.blit(easy, (easyButtonRect.centerx - easy.get_width() / 2, easyButtonRect.centery - easy.get_height() / 2))

    # Create Medium button
    mediumButtonRect = pygame.Rect((Width - buttonWidth) / 2, 300, buttonWidth, buttonHeight)
    mediumButtonColor = BLUE
    pygame.draw.rect(screen, mediumButtonColor, mediumButtonRect)
    medium = menuFont.render("Medium", 1, WHITE)
    screen.blit(medium,
                (mediumButtonRect.centerx - medium.get_width() / 2, mediumButtonRect.centery - medium.get_height() / 2))

    # Create Hard button
    hardButtonRect = pygame.Rect((Width - buttonWidth) / 2, 400, buttonWidth, buttonHeight)
    hardButtonColor = BLUE
    pygame.draw.rect(screen, hardButtonColor, hardButtonRect)
    hard = menuFont.render("Hard", 1, WHITE)
    screen.blit(hard, (hardButtonRect.centerx - hard.get_width() / 2, hardButtonRect.centery - hard.get_height() / 2))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if easyButtonRect.collidepoint(pos):
                    choice = "Easy"
                    d = level_depths[choice]
                    return
                elif mediumButtonRect.collidepoint(pos):
                    choice = "Medium"
                    d = level_depths[choice]
                    return
                elif hardButtonRect.collidepoint(pos):
                    choice = "Hard"
                    d = level_depths[choice]
                    return
            elif event.type == pygame.MOUSEMOTION:
                # Check if mouse is hovering over the buttons
                if easyButtonRect.collidepoint(event.pos):
                    easyButtonColor = LIGHT_BLUE
                else:
                    easyButtonColor = BLUE
                if mediumButtonRect.collidepoint(event.pos):
                    mediumButtonColor = LIGHT_BLUE
                else:
                    mediumButtonColor = BLUE
                if hardButtonRect.collidepoint(event.pos):
                    hardButtonColor = LIGHT_BLUE
                else:
                    hardButtonColor = BLUE

        # Redraw buttons with updated colors
        pygame.draw.rect(screen, easyButtonColor, easyButtonRect)
        screen.blit(easy, (easyButtonRect.centerx - easy.get_width() / 2, easyButtonRect.centery - easy.get_height() / 2))
        pygame.draw.rect(screen, mediumButtonColor, mediumButtonRect)
        screen.blit(medium,
                    (mediumButtonRect.centerx - medium.get_width() / 2, mediumButtonRect.centery - medium.get_height() / 2))
        pygame.draw.rect(screen, hardButtonColor, hardButtonRect)
        screen.blit(hard, (hardButtonRect.centerx - hard.get_width() / 2, hardButtonRect.centery - hard.get_height() / 2))

        pygame.display.update()

board = createBoard()
printBoard(board)
game_over = False

pygame.init()

NRows = 6
NColumns = 7

# Define the size of the board and margins
BoardSize = 95
LeftMargin = 10
RightMargin = 10
TopMargin = 10
BottomMargin = 10

# Calculate the adjusted size of the screen
Width = NColumns * BoardSize + LeftMargin + RightMargin
Height = (NRows + 1) * BoardSize + TopMargin + BottomMargin

# Calculate the adjusted size of the board
AdjustedWidth = NColumns * BoardSize
AdjustedHeight = NRows * BoardSize

# Calculate the adjusted radius
Radius = int(BoardSize / 2 - 5)

# Create the screen with the adjusted size
screen = pygame.display.set_mode((Width, Height))
screen.fill(WHITE)
displayMenu()
screen.fill(WHITE)
drawBoard(board)
pygame.display.update()

turn = random.randint(Computer, Agent)

Font = pygame.font.SysFont("Open Sans", 90)

# start the game
while not game_over:

    # computer turn
    if turn == Computer:
        Score, col = minimax(board, d, False)
        if isValidLocation(board, col).any():
            pygame.time.wait(420)
            row = getChildren(board, col)
            dropPiece(board, row, col, CPiece)

            if winning(board, CPiece):
                label = Font.render(" Computer wins", 1, RED)
                print("Computer wins")
                screen.blit(label, (40, 10))
                game_over = True

            turn += 1
            turn = turn % 2

            printBoard(board)
            drawBoard(board)

    # Agent turn
    if turn == Agent and not game_over:
        Score, col = minimax(board, d, True)
        if isValidLocation(board, col).any():
            pygame.time.wait(200)
            row = getChildren(board, col)
            dropPiece(board, row, col, APiece)

            if winning(board, APiece):
                label = Font.render("Agent wins", 1, BLUE)
                print("Agent wins")
                screen.blit(label, (40, 10))
                game_over = True

            printBoard(board)
            drawBoard(board)

            turn += 1
            turn = turn % 2

    # if the two players tied
    if len(getValidLocations(board)) == 0:
        label = Font.render("The two players tied", 1, BLUE)
        game_over = True
        print("The two players tied")
        screen.blit(label, (40, 10))
        printBoard(board)
        drawBoard(board)

    if game_over:
        pygame.time.wait(3000)