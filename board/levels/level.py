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
    def __init__(self, maze):
        self.maze = maze
        self.rows = len(self.maze)
        self.cols = max(len(row) for row in self.maze)
        self.maze = [row.ljust(self.cols)[:self.cols] for row in self.maze]
        self.board_width = self.cols * tile_size
        self.board_height = self.rows * tile_size
        self.screen_width = self.board_width + 2 * margin
        self.screen_height = self.board_height + header_height + 2 * margin

    # Convert grid coordinates to screen coordinates
    def cell_center(self, row, col):
        # Find horizontal center of tile
        x = margin + col * tile_size + tile_size / 2
        # Find vertical center of tile
        y = margin + (self.rows - 1 - row) * tile_size + tile_size / 2
        return x, y