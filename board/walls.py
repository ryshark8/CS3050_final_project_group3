
import arcade
from config import *

class Wall(arcade.SpriteSolidColor):

    def __init__(self, x, y, tile_size):

        super().__init__(
            width=tile_size+4, height=tile_size+4,
            color=LINE_COLOR,
            center_x=x, center_y=y
        )

class GhostWall(arcade.SpriteSolidColor):

    def __init__(self, x, y, tile_size):

        super().__init__(
            width=tile_size, height=tile_size/4,
            color=LINE_COLOR,
            center_x=x, center_y=y
        )

def build_walls(maze, tile_size, cell_center):

    wall_list = arcade.SpriteList(use_spatial_hash=True)
    ghost_wall_list = arcade.SpriteList()

    for row in range (len(maze)):
        for col in range (len(maze[row])):
            tile = maze[row][col]
            x,y = cell_center(row, col)

            if tile == "#":
                wall = Wall(x, y, tile_size)
                wall_list.append(wall)

            elif tile == "-":
                ghost_wall = GhostWall(x,y,tile_size)
                ghost_wall_list.append(ghost_wall)

    return wall_list, ghost_wall_list