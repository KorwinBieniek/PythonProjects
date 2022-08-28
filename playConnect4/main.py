# finish text version of the game ✅
# Add tests to the text version of the game ✅
# Add graphic menu ✅
# make the game with pygame graphics ✅
# organize code into separate files ✅
# Add easy opponent to play against ✅
# TODO refactor easy computer code
# TODO add graphical menu
# TODO Animate token drop
# TODO add algorithm to play against (hard level)
# TODO give code to refactor

import pygame
import math
import time
import random
from constants import *


def create_board(x, y):
    return [['*' for _ in range(x)] for _ in range(y)]


def print_board(board):
    for row in board:
        print(*row)
    print('_______________')


def drop_token(screen, board, player, column):

    drop_to_row = len(board) - 1
    while board[drop_to_row][column] != '*':
        drop_to_row -= 1
    board[drop_to_row][column] = player
    for r in range(drop_to_row):
        animate_token_drop(player, column, r, screen, SQUARESIZE, RADIUS)


def is_valid_move(board, column):
    if board[0][column] != '*':
        print('You can\'t put a token here!')
        return False
    return True


def check_horizontal(board, player):
    for i in range(COLUMN_COUNT - 3):
        for j in range(ROW_COUNT):
            if board[j][i] == player and board[j][i + 1] == player and board[j][i + 2] == player and board[j][
                i + 3] == player:
                return True
    return False


def check_vertical(board, player):
    for i in range(COLUMN_COUNT):
        for j in range(ROW_COUNT - 3):
            if board[j][i] == player and board[j + 1][i] == player and board[j + 2][i] == player and board[j + 3][
                i] == player:
                return True
    return False


def check_upper_diagonal(board, player):
    for i in range(COLUMN_COUNT - 3):
        for j in range(ROW_COUNT - 3):
            if board[j][i] == player and board[j + 1][i + 1] == player and board[j + 2][i + 2] == player and \
                    board[j + 3][
                        i + 3] == player:
                return True
    return False


def check_lower_diagonal(board, player):
    for i in range(COLUMN_COUNT - 3):
        for j in range(3, ROW_COUNT):
            if board[j][i] == player and board[j - 1][i + 1] == player and board[j - 2][i + 2] == player and \
                    board[j - 3][
                        i + 3] == player:
                return True
    return False


def return_player(player):
    return 'O' if player == 'X' else 'X'


def player_move():
    return int(input('Enter a column where you want to drop a token: ')) - 1


def play_text_game(screen, board):
    player = 'X'
    while True:
        print(f'Now it is {player}\'s turn')
        drop_token(screen, board, player, player_move())
        print_board(board)
        if check_horizontal(board, player) \
                or check_vertical(board, player) \
                or check_upper_diagonal(board, player) \
                or check_lower_diagonal(board, player):
            print(f'Player {player} won the game!')
            break
        player = return_player(player)


def animate_token_drop(player, c, r, screen, SQUARESIZE, RADIUS):
    color = RED if player == 'X' else YELLOW
    pygame.draw.circle(screen, color, (
        int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()
    time.sleep(0.025)
    pygame.draw.circle(screen, WHITE, (
        int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    time.sleep(0.025)
    pygame.display.update()


def draw_board(board, screen, SQUARESIZE, RADIUS):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, WHITE, (
                int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 'X':

                pygame.draw.circle(screen, RED, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), int((r + 1) * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 'O':
                pygame.draw.circle(screen, YELLOW, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), int((r + 1) * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


def check_win(player):
    return check_horizontal(board, player) \
           or check_vertical(board, player) \
           or check_upper_diagonal(board, player) \
           or check_lower_diagonal(board, player)


def calculate_column(screen, width, event):
    pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARESIZE))
    posx = event.pos[0]
    return int(math.floor(posx / SQUARESIZE))


def move_token(screen, width, event, player):
    pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARESIZE))
    posx = event.pos[0]
    if player == 'X':
        pygame.draw.circle(screen, RED, (posx, SQUARESIZE // 2), RADIUS)
    else:
        pygame.draw.circle(screen, YELLOW, (posx, SQUARESIZE // 2), RADIUS)
    pygame.display.update()


def initialize_pygame():
    pygame.init()
    pygame.display.set_caption('ConnectFour')
    return pygame.display.set_mode(SIZE)


def easy_computer(board, screen, MY_FONT):
    game_over = False
    player = 'O'
    col = random.randint(0, 6)
    print(col)
    while True:
        if is_valid_move(board, col):
            drop_token(screen, board, player, col)
            break
        else:
            col = random.randint(0, 6)

    if check_win('O'):
        label = MY_FONT.render("Player 2 wins!", True, YELLOW)
        screen.blit(label, (35, 10))
        game_over = True

    draw_board(board, screen, SQUARESIZE, RADIUS)
    print_board(board)

    if game_over:
        pygame.time.wait(3000)
        exit()


def play_game(board):
    screen = initialize_pygame()
    MY_FONT = pygame.font.SysFont("monospace", 75)
    pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, SQUARESIZE))
    draw_board(board, screen, SQUARESIZE, RADIUS)
    player = 'X'
    game_over = False
    while not game_over:

        if player == 'O':
            easy_computer(board, screen, MY_FONT)
            player = return_player(player)

        else:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    move_token(screen, WIDTH, event, player)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    col = calculate_column(screen, WIDTH, event)


                    if is_valid_move(board, col):
                        drop_token(screen, board, player, col)

                        if check_win(player):
                            if player == 'X':
                                label = MY_FONT.render("Player 1 wins!", True, RED)
                            else:
                                label = MY_FONT.render("Player 2 wins!", True, YELLOW)
                            screen.blit(label, (35, 10))
                            game_over = True

                        draw_board(board, screen, SQUARESIZE, RADIUS)
                        print_board(board)
                        player = return_player(player)

                        if game_over:
                            pygame.time.wait(3000)


board = create_board(COLUMN_COUNT, ROW_COUNT)
if __name__ == '__main__':
    play_game(board)
