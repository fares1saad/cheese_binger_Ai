from PIL import ImageGrab
import pyautogui

# YOU MAY NEED TO CHANGE THESE VALUES BASED ON YOUR SCREEN SIZE
LEFT = 581
TOP = 230
RIGHT = 1335
BOTTOM = 875

EMPTY = 0
RED = 1
BLUE = 2


class Board:
    def __init__(self) -> None:
        self.board = [[EMPTY for _ in range(7)] for _ in range(6)]

    @staticmethod
    def print_grid(grid):
        for i in range(0, len(grid)):
            for j in range(0, len(grid[i])):
                if grid[i][j] == EMPTY:
                    print("*", end=" \t")
                elif grid[i][j] == RED:
                    print("R", end=" \t")
                elif grid[i][j] == BLUE:
                    print("B", end=" \t")
            print("\n")

    @staticmethod
    def _convert_grid_to_color(grid):
        for i in range(0, len(grid)):
            for j in range(0, len(grid[i])):
                if grid[i][j] == (255, 255, 255):
                    grid[i][j] = EMPTY
                elif grid[i][j][0] > 200:
                    grid[i][j] = RED
                elif grid[i][j][0] > 40:
                    grid[i][j] = BLUE
        return grid

    @staticmethod
    def _get_grid_coordinates():
        startCord = (50, 55)
        cordArr = []
        for i in range(0, 7):
            for j in range(0, 6):
                x = startCord[0] + i * 115
                y = startCord[1] + j * 112
                cordArr.append((x, y))
        return cordArr

    @staticmethod
    def _transpose_grid(grid):
        return [[grid[j][i] for j in range(len(grid))] for i in range(len(grid[0]))]

    @staticmethod
    def _capture_image():
        image = ImageGrab.grab()
        croppedImage = image.crop((LEFT, TOP, RIGHT, BOTTOM))
        return croppedImage

    def _convert_image_to_grid(self, image):
        pixels = [[] for _ in range(7)]
        i = 0
        for index, cord in enumerate(self._get_grid_coordinates()):
            pixel = image.getpixel(cord)
            if index % 6 == 0 and index != 0:
                i += 1
            pixels[i].append(pixel)
        return pixels

    def _get_grid(self):
        cropped_image = self._capture_image()
        pixels = self._convert_image_to_grid(cropped_image)
        # cropped_image.show()
        grid = self._transpose_grid(pixels)
        return grid

    def _check_if_game_end(self, grid):
        for i in range(0, len(grid)):
            for j in range(0, len(grid[i])):
                if grid[i][j] == EMPTY and self.board[i][j] != EMPTY:
                    return True
        return False

    def get_game_grid(self):
        game_grid = self._get_grid()
        new_grid = self._convert_grid_to_color(game_grid)
        is_game_end = self._check_if_game_end(new_grid)
        self.board = new_grid
        return self.board, is_game_end

    def select_column(self, column):
        pyautogui.click(LEFT + self._get_grid_coordinates()[column * 6][0], TOP)
