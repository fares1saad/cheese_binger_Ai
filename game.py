import numpy as np
from board import Board
import time
import random
import math
import tkinter as tk
from tkinter import ttk

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
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece \
                    and board[r][c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece \
                    and board[r + 3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece \
                    and board[r + 3][c + 3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece \
                    and board[r - 3][c + 3] == piece:
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

    # Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score positive sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


def minimax(board, depth, maximize):
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
            new_score = minimax(b_copy, depth - 1, False)[1]

            if new_score > value:
                value = new_score
                column = col

        return column, value

    else:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = free_row(board, col)

            b_copy = board.copy()
            b_copy[row][col] = PLAYER_PIECE
            new_score = minimax(b_copy, depth - 1, True)[1]

            if new_score < value:
                value = new_score
                column = col

        return column, value


def main():
    board = Board()

    def handle_click():
        window.destroy()

    window = tk.Tk()

    window.title("Connect-4 Game Settings")
    window.geometry("500x300")
    window.configure(bg="#1e1e1e")

    # Define the options for the dropdown menus
    difficulty_options = ["Easy", "Medium", "Hard"]
    algorithm_options = ["Minimax", "Alpha-Beta Pruning"]

    # Create a StringVar to store the selected options
    selected_difficulty = tk.StringVar()
    selected_algorithm = tk.StringVar()

    # Create a style for the labels and buttons
    style = ttk.Style()
    style.configure("TLabel", foreground="#fff", background="#1e1e1e", font=("Comic Sans MS", 12))
    style.configure("TButton", foreground="#000", background="#4a4a4a", font=("Comic Sans MS", 12))

    # Create a label for the dropdown menu
    label_difficulty = ttk.Label(window, text="Select Difficulty:")
    label_difficulty.pack(pady=10)

    # Create a dropdown menu with the difficulty options and the selected_difficulty variable
    dropdown_difficulty = ttk.Combobox(window, values=difficulty_options, textvariable=selected_difficulty)
    dropdown_difficulty.pack()

    # Create a label for the algorithm dropdown menu
    label_algorithm = ttk.Label(window, text="Select Algorithm:")
    label_algorithm.pack(pady=10)

    # Create a dropdown menu with the algorithm options and the selected_algorithm variable
    dropdown_algorithm = ttk.Combobox(window, values=algorithm_options, textvariable=selected_algorithm)
    dropdown_algorithm.pack()

    # Create a button to submit the selections and call the handle_click function
    button_submit = ttk.Button(window, text="Start Game", command=handle_click)
    button_submit.pack(pady=20)

    # Start the main loop
    window.mainloop()

    time.sleep(2)
    game_end = False

    difficulty = 1

    minmax_total_times = []
    alpha_beta_total_times = []

    d = selected_difficulty.get()

    if d == "Easy":
        difficulty = 1
    elif d == "Medium":
        difficulty = 3
    else:
        difficulty = 5

    alg = selected_algorithm.get()

    if alg == "Minimax":
        while not game_end:

            (game_board, game_end) = board.get_game_grid()

            # FOR DEBUG PURPOSES
            board.print_grid(game_board)
            print(game_board)

            # YOUR CODE GOES HERE

            arr = np.array(game_board)
            # score = score_position(arr, 1)
            board1 = arr.copy()

            for j in range(6):
                board1[j] = arr[5 - j]

            print(selected_algorithm.get())
            print("mini")
            minimax_start_time = time.time()
            column, score = minimax(board1, difficulty, True)
            minimax_end_time = time.time()
            print("the selected column is:")
            print(column)

            minimax_total_time = minimax_end_time - minimax_start_time
            minmax_total_times.append(minimax_total_time)

            board.select_column(column)

            print(board1)
            print(minmax_total_times)

            # Insert here the action you want to perform based on the output of the algorithm
            # You can use the following function to select a column

            time.sleep(2)

    else:
        while not game_end:

            (game_board, game_end) = board.get_game_grid()

            # FOR DEBUG PURPOSES
            board.print_grid(game_board)
            print(game_board)

            # YOUR CODE GOES HERE

            arr = np.array(game_board)
            # score = score_position(arr, 1)
            board1 = arr.copy()

            for i in range(6):
                board1[i] = arr[5 - i]

            print(selected_algorithm.get())
            print("alpha")
            alpha_start_time = time.time()
            column, score = minimax_alpha(board1, difficulty, -math.inf, math.inf, True)
            alpha_end_time = time.time()

            alpha_total_time = alpha_end_time - alpha_start_time
            alpha_beta_total_times.append(alpha_total_time)

            print("the selected column is:")
            print(column)

            board.select_column(column)

            print(board1)
            print(alpha_beta_total_times)

            # Insert here the action you want to perform based on the output of the algorithm
            # You can use the following function to select a column

            time.sleep(2)


if __name__ == "__main__":
    main()
