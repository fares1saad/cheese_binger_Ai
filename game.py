from board import Board
import time
import random
import math

# import numpy as np

# GAME LINK
# http://kevinshannon.com/connect4/

EMPTY = 0

PLAYER_PIECE = 2
AI_PIECE = 1
ROW_COUNT = 6
COLUMN_COUNT = 7
WINDOW_LENGTH = 4
WINNING_LENGTH = 4


def free_row(board, col):
    for r in range(ROW_COUNT):  # check for the next free row
        if board[r][col] == 0:
            return r


def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True


def is_board_full(board):
    for col in range(COLUMN_COUNT):
        if board[ROW_COUNT - 1][col] == 0:
            return False
    return True


# def playable_places(board):
#     valid_locations = []
#     for col in range(COLUMN_COUNT):
#         if np.any(board[:, col] == 0):
#             valid_locations.append(col)
#     return valid_locations

def is_valid_location(board, col):
    for row in range(ROW_COUNT):
        if board[row][col] == 0:
            return True
    return False


def playable_places(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations





def evaluate_window(window, piece):
    piece = 1
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 50  # Attack score
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5  # Attack score
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2  # Attack score

    if window.count(opp_piece) == 4:
        score -= 50  # Defense score
    elif window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 5  # Defense score
    elif window.count(opp_piece) == 2 and window.count(EMPTY) == 2:
        score -= 2  # Defense score

    return score


def score_position(board, piece):
    board = np.array(board)
    score = 0

    ## Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    ## Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score posiive sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

def minimax_alpha(board, depth, alpha, beta, maximize):
    valid_locations = playable_places(board)

    is_terminal = True if winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or is_board_full(
        board) else False

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return None, 1000000
            elif winning_move(board, PLAYER_PIECE):
                return None, -1000000
            else:
                return None, 0
        else:
            return None, score_position(board, AI_PIECE)

    if maximize:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = free_row(board, col)

            b_copy = board.copy()
            b_copy[row][col] = AI_PIECE
            new_score = minimax_alpha(b_copy, depth - 1, alpha, beta, False)[1]

            if new_score > value:
                value = new_score
                column = col

            alpha = max(alpha, value)
            if alpha >= beta:
                break

        return column, value

    else:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = free_row(board, col)

            b_copy = board.copy()
            b_copy[row][col] = PLAYER_PIECE
            new_score = minimax_alpha(b_copy, depth - 1, alpha, beta, True)[1]

            if new_score < value:
                value = new_score
                column = col

            beta = min(beta, value)
            if alpha >= beta:
                break

        return column, value

def minimax(board, depth, maximize):
    # Where ("difficulty" is the depth the Ai can reach) and ("maximize" is
    # the decision of whether to maximize the score or minimize it)

    valid_locations = playable_places(board)

    is_terminal = True if winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or is_board_full(
        board) else False

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return None, 1000000
            elif winning_move(board, PLAYER_PIECE):
                return None, -1000000
            else:  # Game is over, no more valid moves
                return None, 0
        else:  # Depth is zero
            return None, score_position(board, AI_PIECE)

    if maximize:  # Maximize the goal score

        value = -math.inf  # initialize to a very small value
        column = random.choice(valid_locations)

        for col in valid_locations:
            row = free_row(board, col)

            b_copy = board.copy()
            b_copy[row][col] = AI_PIECE
            new_score = minimax(b_copy, depth - 1, False)[1]

            if new_score > value:
                value = new_score
                column = col
        return column, value

    else:  # Minimize the goal score
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = free_row(board, col)

            b_copy = board.copy()
            b_copy[row][col] = PLAYER_PIECE  # simulate the action of playing the piece
            new_score = minimax(b_copy, depth - 1, True)[1]

            if new_score < value:
                value = new_score
                column = col

        return column, value


def free_row(board, col):
    for r in range(ROW_COUNT):  # check for the next free row
        if board[r][col] == 0:
            return r


def main():
    board = Board()

    difficulty = 4

    time.sleep(2)
    game_end = False

    while not game_end:

        (game_board, game_end) = board.get_game_grid()

        # FOR DEBUG PURPOSES
        board.print_grid(game_board)

        # YOUR CODE GOES HERE

        # arr = np.array(game_board)
        # score = score_position(arr, 1)

        random_column, temp_score = minimax(game_board, difficulty, True)  # minimax :)
        board.select_column(random_column)

        print(game_board)

        # Insert here the action you want to perform based on the output of the algorithm
        # You can use the following function to select a column

        time.sleep(2)


if __name__ == "__main__":
    main()
