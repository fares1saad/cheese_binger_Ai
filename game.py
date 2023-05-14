from board import Board
import time
import random
import math

# GAME LINK
# http://kevinshannon.com/connect4/

EMPTY = 0

def is_all_full(lst):
    return all(x != EMPTY for x in lst)


# Checks if the board is full before any move
def is_Board_full(board):
    for i in range(6):
        if not is_all_full(board[i]):
            return False
    return True


# checks if a column is full
def Valid_move(board, col):
    for i in range(5, 0, -1):
        if board[i][col] == EMPTY:
            return True
    return False



def MinMax(game_board):
    fes =1+1


def main():
    board = Board()

    time.sleep(2)
    game_end = False
    while not game_end:
        (game_board, game_end) = board.get_game_grid()

        # FOR DEBUG PURPOSES
        board.print_grid(game_board)

        # YOUR CODE GOES HERE

        # Insert here the action you want to perform based on the output of the algorithm
        # You can use the following function to select a column
        random_column = random.randint(0, 6)

        board.select_column(random_column)

        time.sleep(2)


if __name__ == "__main__":
    main()
