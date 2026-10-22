"""
Script for creating gameboard
"""

import arcade

from config import *
from board.walls import build_walls

class PacmanBoard:
    def __init__(self, level):

        self.level = level

        maze = self.level.maze
        tile_size = self.level.tile_size
        cell_center = self.level.cell_center
        label_size = self.level.label_size
        score_size = self.level.score_size
        label_position = self.level.label_position
        score_position = self.level.score_position
        high_score_position = self.level.high_score_position
        margin = self.level.margin
        header_height = self.level.header_height
        rows = self.level.rows
        cols = self.level.cols

        screen_width = self.level.screen_width
        screen_height = self.level.screen_height
        board_width = self.level.board_width
        board_height = self.level.board_height

        self.wall_list, self.ghost_wall_list = build_walls(
            maze, tile_size, cell_center)

        self.high_score_label = arcade.Text(
            "HIGH SCORE",
            screen_width / 2,
            margin + board_height + label_position,
            arcade.color.WHITE,
            font_size = label_size,
            anchor_x = "center"
        )

        # Create the high-score number.
        self.high_score_number = arcade.Text(
            "140",
            screen_width / 2,
            margin + board_height + high_score_position,
            arcade.color.WHITE,
            font_size = score_size,
            anchor_x = "center"
        )

        self.current_score_label = arcade.Text(
            "CURRENT SCORE",
            margin + score_position,
            margin + board_height + label_position,
            arcade.color.WHITE,
            font_size = label_size,
            anchor_x = "center"
        )

        # Create the current-score number on the left.
        self.current_score_number = arcade.Text(
            "0",
            margin + score_position,
            margin + board_height + high_score_position,
            arcade.color.WHITE,
            font_size = score_size,
            anchor_x = "center"
        )

    # Draw maze
    def draw_maze(self):

        self.wall_list.draw()
        self.ghost_wall_list.draw()

        # Wall outline
        for wall in self.wall_list:
            arcade.draw_rect_filled(
                arcade.XYWH(
                    wall.center_x, wall.center_y,
                    self.level.tile_size, self.level.tile_size
                ),
                color=FILL_COLOR
            )

    def draw_header(self):
        # Draw the existing text objects on the screen.
        self.high_score_label.draw()
        self.high_score_number.draw()
        self.current_score_label.draw()
        self.current_score_number.draw()

    def draw(self):
        self.draw_maze()
        self.draw_header()