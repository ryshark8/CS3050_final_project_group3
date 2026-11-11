"""
Dot Sprites
"""

import arcade

from config import (TILE_SIZE, LABEL_SIZE, SCORE_SIZE, LABEL_POSITION,
                    SCORE_POSITION, HIGH_SCORE_POSITION, MARGIN, HEADER_HEIGHT)

tile_size = TILE_SIZE
label_size = LABEL_SIZE
score_size = SCORE_SIZE
label_position = LABEL_POSITION
score_position = SCORE_POSITION
high_score_position = HIGH_SCORE_POSITION
margin = MARGIN
header_height = HEADER_HEIGHT


class MegaDot:
    def __init__(self):

        self.mega_dot_list = arcade.SpriteList()

    def create_mega_dots(self, level):

        self.mega_dot_list.clear()

        for row in range(level.rows):
            for col in range(level.cols):
                if level.maze[row][col] == "@":
                    x, y = level.cell_center(row, col)

                    dot_radius = max(6, int(tile_size / 3))

                    dot = arcade.SpriteCircle(dot_radius, arcade.color.YELLOW)
                    dot.center_x = x
                    dot.center_y = y

                    self.mega_dot_list.append(dot)

        return self.mega_dot_list