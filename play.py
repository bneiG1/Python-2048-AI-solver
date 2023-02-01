from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import sys, pygame
import game
from ai import *
import multiprocessing as mp

ai = False
depth = 2

# UI
size = width, height = 800, 820
playRegion = 800, 800
FPS = 60

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
fontColor = (82, 52, 42)
defaultTileColor = (204, 192, 179)
tileBoarderColor = (82, 52, 42)

# Game
boardSize = 4


def drawBoard(screen, board):
    screen.fill(black)
    box = 800 // 4
    padding = 5
    for i in range(board.boardSize):
        for j in range(board.boardSize):
            color = defaultTileColor
            fontColor = (82, 52, 42)
            numberText = ''
            if board.board[i][j] != 0:

                numberText = str(board.board[i][j])

                if (numberText == '2'):
                    color = (238, 228, 218)
                    fontColor = (82, 52, 42)
                if (numberText == '4'):
                    color = (237, 224, 200)
                    fontColor = (82, 52, 42)
                if (numberText == '8'):
                    color = (242, 177, 121)
                    fontColor = (238, 228, 218)
                if (numberText == '16'):
                    color = (245, 149, 99)
                    fontColor = (238, 228, 218)
                if (numberText == '32'):
                    color = (246, 124, 95)
                    fontColor = (238, 228, 218)
                if (numberText == '64'):
                    color = (246, 94, 59)
                    fontColor = (238, 228, 218)
                if (numberText == '128'):
                    color = (237, 207, 114)
                    fontColor = (238, 228, 218)
                if (numberText == '256'):
                    color = (237, 204, 97)
                    fontColor = (238, 228, 218)
                if (numberText == '512'):
                    color = (237, 200, 80)
                    fontColor = (238, 228, 218)
                if (numberText == '1024'):
                    color = (237, 197, 63)
                    fontColor = (238, 228, 218)
                if (numberText == '2048'):
                    color = (237, 194, 46)
                    fontColor = (238, 228, 218)
                if (
                        numberText != '2048' and numberText != '1024' and numberText != '512' and numberText != '256' and numberText != '128' and numberText != '64' and numberText != '32' and numberText != '16' and numberText != '8' and numberText != '4' and numberText != '2'):
                    color = (0, 0, 0)
                    fontColor = (238, 228, 218)

            rect = pygame.draw.rect(screen, color, (j * box + padding,
                                                    i * box + padding,
                                                    box - 2 * padding,
                                                    box - 2 * padding), 0)

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, fontColor, rect, 1)

            fontImage = tileFont.render(numberText, 0, fontColor)
            if fontImage.get_width() > playRegion[0] / board.boardSize:
                fontImage = pygame.transform.scale(fontImage,
                                                   (playRegion[0] / board.boardSize,
                                                    fontImage.get_height() / fontImage.get_width() * playRegion[
                                                        0] / board.boardSize))

            screen.blit(fontImage,
                        (j * playRegion[0] / board.boardSize + (
                                    playRegion[0] / board.boardSize - fontImage.get_width()) / 2,
                         i * playRegion[1] / board.boardSize + (
                                     playRegion[1] / board.boardSize - fontImage.get_height()) / 2))

    fontImage = scoreFont.render(
        "[Arrows or W,A,S,D-directions, Space-activate AI, R-restart, Esc-quit]   Score: {:,}".format(board.score) + (
            " [AI enabled, depth={}]".format(depth) if ai else ""), 1, white)

    if (board.checkLoss()):
        fontImage = scoreFont.render(
            "Score: {:,}".format(board.score) + (" [AI enabled, depth={}]".format(depth) if ai else "") + " GAME OVER!",
            1, white)

    screen.blit(fontImage, (1, playRegion[1] + 1))


def handleInput(event, board):
    global ai

    if event.type == pygame.QUIT:
        pool.close()
        pool.terminate()
        sys.exit()

    if event.type == pygame.KEYDOWN:

        if event.key == pygame.K_RIGHT:
            board.move(game.RIGHT)
        elif event.key == pygame.K_LEFT:
            board.move(game.LEFT)
        elif event.key == pygame.K_UP:
            board.move(game.UP)
        elif event.key == pygame.K_DOWN:
            board.move(game.DOWN)
        if event.key == pygame.K_r:
            board = game.Board(boardSize)
        elif event.key == pygame.K_ESCAPE:
            pool.close()
            pool.terminate()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            ai = not ai

    return board


def gameLoop():
    global depth
    clock = pygame.time.Clock()
    board = game.Board(boardSize)

    while 1:
        for event in pygame.event.get():
            board = handleInput(event, board)

        if ai and not board.checkLoss():
            nextBestMove = getNextBestMoveExpectiminimax(board, pool, depth)
            board.move(nextBestMove)
            print(board)

        drawBoard(screen, board)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    global screen
    global tileFont
    global scoreFont
    global pool

    mp.freeze_support()
    mp.set_start_method('spawn')
    pool = mp.Pool(processes=8)

    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("2048")
    tileFont = pygame.font.SysFont("", 72)
    scoreFont = pygame.font.SysFont("", 22)
    gameLoop()
