import random

EMPTY_SYMBOL = ' '
X_SYMBOL = 'X'
O_SYMBOL = 'O'


class AlreadyTakenSpotError(Exception):
    """Raised when one of the indexes is already taken"""
    pass


class Board:
    pass


def return_cells(board):
    s = '---------\n'
    for row in board:
        s += '| '
        for place in row:
            s += f'{place} '
        s += '|'
        s += "\n"
    s += '---------'
    return s


def _create_board():
    rows = []
    for i in range(3):
        row = []
        for _ in range(3):
            row.append(' ')
        rows.append(row)
    return rows


def fix_spot(board, player, row_index, col_index):
    if board[row_index][col_index] != ' ':
        raise AlreadyTakenSpotError()
    else:
        board[row_index][col_index] = player


def _verify_coordinates(board, player):
    while True:
        try:
            row, col = list(
                map(int, input('Enter the coordinates: ').split()))
            fix_spot(board, player, row_index=row - 1, col_index=col - 1)
            break
        except AlreadyTakenSpotError:
            print('This cell is occupied! Choose another one!')
            continue
        except IndexError:
            print('Coordinates should be from 1 to 3!')
            continue
        except ValueError:
            print('You should enter numbers!')
            continue


def is_win(board, player):
    return bool(_check_rows(board, player, len(board))
                or _check_columns(board, player, len(board))
                or _check_diagonals(board, player, len(board)))


def is_draw(board):
    for row in board:
        for place in row:
            if place == ' ':
                return False
    return True


def _check_rows(board, player, board_length):
    for i in range(board_length):
        if win := all(board[i][j] == player for j in range(board_length)):
            return win


def _check_columns(board, player, board_length):
    for i in range(board_length):
        if win := all(board[j][i] == player for j in range(board_length)):
            return win


def _check_diagonals(board, player, board_length):
    win = True
    for i in range(board_length):
        win = True
        if board[i][i] != player:
            win = False
            break
    if win:
        return win

    for i in range(board_length):
        win = True
        if board[i][board_length - 1 - i] != player:
            win = False
            break
    if win:
        return win
    return False


def computer_easy(board, player):
    print('Making move level "easy"')
    while True:
        row = random.randint(0, 2)
        column = random.randint(0, 2)
        if board[row][column] == ' ':
            break
    fix_spot(board, player, row, column)


def computer_medium(board):
    places = [(0, 0), (0, 1), (0, 2),
              (1, 0), (1, 1), (1, 2),
              (2, 0), (2, 1), (2, 2)]
    print('Making move level "medium"')
    for place in places:
        if board[place[0]][place[1]] == ' ':
            fix_spot(board, O_SYMBOL, place[0], place[1])
            flag = is_win(board, O_SYMBOL)
            if flag:
                # print('I see enemy win')
                board[place[0]][place[1]] = ' '
                return place[0], place[1]
            else:
                board[place[0]][place[1]] = ' '

            fix_spot(board, X_SYMBOL, place[0], place[1])
            flag = is_win(board, X_SYMBOL)
            if flag:
                # print('I see my win')
                board[place[0]][place[1]] = ' '
                return place[0], place[1]
            else:
                board[place[0]][place[1]] = ' '
    # print('I go random')
    while True:
        row = random.randint(0, 2)
        column = random.randint(0, 2)
        if board[row][column] == ' ':
            return row, column


# Python3 program to find the next optimal move for a player
player, opponent = 'X', 'O'


# This function returns true if there are moves
# remaining on the board. It returns false if
# there are no moves left to play.
def isMovesLeft(board):
    for i in range(3):
        for j in range(3):
            if (board[i][j] == ' '):
                return True
    return False


# This is the evaluation function as discussed
# in the previous article ( http://goo.gl/sJgv68 )
def evaluate(b):
    # Checking for Rows for X or O victory.
    for row in range(3):
        if (b[row][0] == b[row][1] and b[row][1] == b[row][2]):
            if (b[row][0] == player):
                return 10
            elif (b[row][0] == opponent):
                return -10

    # Checking for Columns for X or O victory.
    for col in range(3):

        if (b[0][col] == b[1][col] and b[1][col] == b[2][col]):

            if (b[0][col] == player):
                return 10
            elif (b[0][col] == opponent):
                return -10

    # Checking for Diagonals for X or O victory.
    if (b[0][0] == b[1][1] and b[1][1] == b[2][2]):

        if (b[0][0] == player):
            return 10
        elif (b[0][0] == opponent):
            return -10

    if (b[0][2] == b[1][1] and b[1][1] == b[2][0]):

        if (b[0][2] == player):
            return 10
        elif (b[0][2] == opponent):
            return -10

    # Else if none of them have won then return 0
    return 0


# This is the minimax function. It considers all
# the possible ways the game can go and returns
# the value of the board
def minimax(board, depth, isMax):
    score = evaluate(board)

    # If Maximizer has won the game return his/her
    # evaluated score
    if (score == 10):
        return score

    # If Minimizer has won the game return his/her
    # evaluated score
    if (score == -10):
        return score

    # If there are no more moves and no winner then
    # it is a tie
    if (isMovesLeft(board) == False):
        return 0

    # If this maximizer's move
    if (isMax):
        best = -1000

        # Traverse all cells
        for i in range(3):
            for j in range(3):

                # Check if cell is empty
                if (board[i][j] == ' '):
                    # Make the move
                    board[i][j] = player

                    # Call minimax recursively and choose
                    # the maximum value
                    best = max(best, minimax(board,
                                             depth + 1,
                                             not isMax))

                    # Undo the move
                    board[i][j] = ' '
        return best

    # If this minimizer's move
    else:
        best = 1000

        # Traverse all cells
        for i in range(3):
            for j in range(3):

                # Check if cell is empty
                if (board[i][j] == ' '):
                    # Make the move
                    board[i][j] = opponent

                    # Call minimax recursively and choose
                    # the minimum value
                    best = min(best, minimax(board, depth + 1, not isMax))

                    # Undo the move
                    board[i][j] = ' '
        return best


# This will return the best possible move for the player
def findBestMove(board):
    bestVal = -1000
    bestMove = (-1, -1)

    # Traverse all cells, evaluate minimax function for
    # all empty cells. And return the cell with optimal
    # value.
    for i in range(3):
        for j in range(3):

            # Check if cell is empty
            if (board[i][j] == ' '):

                # Make the move
                board[i][j] = player

                # compute evaluation function for this
                # move.
                moveVal = minimax(board, 0, False)

                # Undo the move
                board[i][j] = ' '

                # If the value of the current move is
                # more than the best value, then update
                # best/
                if (moveVal > bestVal):
                    bestMove = (i, j)
                    bestVal = moveVal

    print("The value of the best Move is :", bestVal)
    print()
    return bestMove


def is_finished(board, player):
    if is_win(board, player):
        print(f'{player} wins')
        return True
    elif is_draw(board):
        print('Draw')
        return True
    return False


def game_mode():
    player_one = 0
    player_two = 0
    while True:
        if player_one != 0 and player_two != 0:
            return player_one, player_two
        game_type = input('Input command: > ').split()
        if game_type[0] == 'start':
            try:
                if game_type[1] == 'user':
                    player_one = 1
                elif game_type[1] == 'easy':
                    player_one = 2
                elif game_type[1] == 'medium':
                    player_one = 3
                elif game_type[1] == 'hard':
                    player_one = 4

                if game_type[2] == 'user':
                    player_two = 1
                elif game_type[2] == 'easy':
                    player_two = 2
                elif game_type[2] == 'medium':
                    player_two = 3
                elif game_type[2] == 'hard':
                    player_two = 4

            except IndexError:
                print('Bad parameters!')
                continue
        elif game_type[0] == 'exit':
            exit(0)
        else:
            print('Bad parameters!')
            continue


def main():
    pl_one, pl_two = game_mode()
    board = _create_board()
    print(return_cells(board))

    while True:
        player = X_SYMBOL
        second_player = O_SYMBOL
        if pl_one == 1:
            _verify_coordinates(board, player)
        elif pl_one == 2:
            computer_easy(board, player)
        elif pl_one == 3:
            row, col = computer_medium(board)
            fix_spot(board, player, row, col)
        elif pl_one == 4:
            # computer_hard(board, player, second_player)
            bestMove = findBestMove(board)
            fix_spot(board, player, bestMove[0], bestMove[1])

        print(return_cells(board))
        if is_finished(board, 'X'):
            break

        if pl_two == 1:
            _verify_coordinates(board, second_player)
        elif pl_two == 2:
            computer_easy(board, second_player)
        elif pl_two == 3:
            row, col = computer_medium(board)
            fix_spot(board, second_player, row, col)
        elif pl_two == 4:
            # computer_hard(board, second_player, player)
            bestMove = findBestMove(board)
            fix_spot(board, second_player, bestMove[0], bestMove[1])

        print(return_cells(board))
        if is_finished(board, 'O'):
            break


if __name__ == '__main__':
    main()
