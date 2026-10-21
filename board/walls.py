
import arcade
from config import *

class Wall(arcade.SpriteSolidColor):

    def __init__(self, x, y, tile_size):

        super().__init__(
            width=tile_size+4, height=tile_size+4,
            color=LINE_COLOR,
            center_x=x, center_y=y
        )

        # Create Walls
        def create_walls(self):
            for row in range(self.rows):
                for col in range(self.cols):
                    if self.maze[row][col] == "#":
                        x, y = self.cell_center(row, col)

                        wall = Wall(x, y, self.tile_size)

                        self.wall_list.append(wall)


class GhostWall(arcade.SpriteSolidColor):

    def __init__(self, x, y, tile_size):

        super().__init__(
            width=tile_size, height=tile_size/4,
            color=LINE_COLOR,
            center_x=x, center_y=y
        )

        # Create Walls
        def create_walls(self):
            for row in range(self.rows):
                for col in range(self.cols):
                    if self.maze[row][col] == "-":
                        x, y = self.cell_center(row, col)

                        wall = GhostWall(x, y, self.tile_size)

                        self.ghost_wall_list.append(wall)
