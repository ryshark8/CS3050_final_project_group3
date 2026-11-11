"""
File for Level Class
Calculates board dimensions for a specific level and
has cell center function
"""

from config import *

tile_size = TILE_SIZE
label_size = LABEL_SIZE
score_size = SCORE_SIZE
label_position = LABEL_POSITION
score_position = SCORE_POSITION
high_score_position = HIGH_SCORE_POSITION
margin = MARGIN
header_height = HEADER_HEIGHT


class Level:
    def __init__(self, maze, name="level"):
        self.maze = maze
        self.rows = len(self.maze)
        self.cols = max(len(row) for row in self.maze)
        self.maze = [row.ljust(self.cols)[: self.cols] for row in self.maze]
        self.board_width = self.cols * tile_size + TILE_SIZE
        self.board_height = self.rows * tile_size
        self.screen_width = self.board_width
        self.screen_height = self.board_height + header_height + 2 * margin

        if DEBUG:
            print(f"[{name}] Rows: {self.rows}, Columns: {self.cols}, "
                  f"Screen: {self.screen_width}x{self.screen_height}")

    # ---------------------- Ross edit ---------------------------
    # Convert grid coordinates to screen coordinates
    def cell_center(self, row, col):
        # Find horizontal center of tile
        x = (col + 1) * tile_size
        # Find vertical center of tile
        y = (self.rows - row) * tile_size
        return x, y

    def find_tile(self, char):
        """Returns the screen (x, y) coordinates for a specific char in the maze"""
        for row, line in enumerate(self.maze):
            col = line.find(char)
            if col != -1:
                return self.cell_center(row, col)
        return None

    def find_jail_center(self):
        return self.find_tile("*")

    # def find_jail_center(self):
    #     jail_center = None
    #
    #     for row in range(len(self.maze)):
    #         for col in range(len(self.maze[row])):
    #             tile = self.maze[row][col]
    #
    #             if tile == "*":
    #                 jail_center = (row * TILE_SIZE, (col * TILE_SIZE))
    #
    #     # jail_center = (self.board_height/2, self.board_width)
    #
    #     return jail_center
