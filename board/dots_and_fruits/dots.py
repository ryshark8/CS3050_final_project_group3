"""
Dot Sprites
"""
import arcade


class Dot:
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

        self.dot_list = arcade.SpriteList()


    def create_dots(self):

        for row in range(self.rows):
            for col in range(self.cols):
                if self.maze[row][col] == "#":
                    x, y = self.cell_center(row, col)

                    wall = Wall(x,y, self.tile_size)

                    self.wall_list.append(wall)
