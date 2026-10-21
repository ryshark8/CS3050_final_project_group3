"""
Script for creating gameboard
"""

import arcade

from config import *
from levels.level import *
from levels import level1_board
from walls import *

# Create window

class PacmanBoard:
    def __init__(self, level):

        self.level = level

        self.tile_size = level.tile_size
        self.label_size = level.label_size
        self.score_size = level.score_size
        self.label_position = level.label_position
        self.score_position = level.score_position
        self.high_score_position = level.high_score_position
        self.margin = level.margin
        self.header_height = level.header_height
        self.rows = level.rows
        self.cols = level.cols
        self.maze = level.maze
        self.screen_width = level.screen_width
        self.screen_height = level.screen_height
        self.board_width = level.board_width
        self.board_height = level.board_height


        self.wall_list = arcade.SpriteList()
        self.ghost_wall_list = arcade.SpriteList()

        self.create_walls()

        self.high_score_label = arcade.Text(
            "HIGH SCORE",
            self.screen_width / 2,
            self.margin + self.board_height + self.label_position,
            arcade.color.WHITE,
            font_size = self.label_size,
            anchor_x = "center"
        )

        # Create the high-score number.
        self.high_score_number = arcade.Text(
            "140",
            self.screen_width / 2,
            self.margin + self.board_height + self.high_score_position,
            arcade.color.WHITE,
            font_size = self.score_size,
            anchor_x = "center"
        )

        self.current_score_label = arcade.Text(
            "CURRENT SCORE",
            self.margin + self.score_position,
            self.margin + self.board_height + self.label_position,
            arcade.color.WHITE,
            font_size = self.label_size,
            anchor_x = "center"
        )

        # Create the current-score number on the left.
        self.current_score = arcade.Text(
            "0",
            self.margin + self.score_position,
            self.margin + self.board_height + self.high_score_position,
            arcade.color.WHITE,
            font_size = self.score_size,
            anchor_x = "center"
        )

    def setup_level1(self):
        level1 = Level(TILE_SIZE, LABEL_SIZE, SCORE_SIZE, LABEL_POSITION, SCORE_POSITION,
                       HIGH_SCORE_POSITION, MARGIN, HEADER_HEIGHT, level1_board.rows, level1_board.cols,
                       level1_board.maze, level1_board.screen_width, level1_board.screen_height,
                       level1_board.board_width, level1_board.board_height)

        level1.board = PacmanBoard(level1)

        level1.wall_list = level1.board.wall_list
        level1.ghost_wall_list = level1.board.ghost_wall_list

        return level1

    # Convert grid coordinates to screen coordinates
    def cell_center(self, row, col):
        # Find horizontal center of tile
        x = self.margin + col * self.tile_size + self.tile_size / 2
        # Find vertical center of tile
        y = self.margin + (self.rows - 1 - row) * self.tile_size + self.tile_size / 2
        return x, y

    # Draw maze
    def draw_maze(self):

        self.wall_list.draw()
        self.ghost_wall_list.draw()

        # Wall outline
        for wall in self.wall_list:
            arcade.draw_rect_filled(
                arcade.XYWH(
                    wall.center_x, wall.center_y,
                    self.tile_size, self.tile_size
                ),
                color=FILL_COLOR
            )

    def draw_header(self):
        # Draw the existing text objects on the screen.
        self.high_score_label.draw()
        self.high_score_number.draw()
        self.current_score_label.draw()
        self.current_score.draw()
