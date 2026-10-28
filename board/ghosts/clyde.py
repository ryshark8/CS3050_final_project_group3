import arcade
from pathlib import Path
from board.ghosts.ghost import Ghost
from config import *

class Clyde(Ghost):

    JAIL_TIME = 15

    #TODO: create a dictionary of attributes based on color of the ghost
    def __init__(self, barrier_list, jail_center):

        super().__init__(barrier_list, jail_center)

        sprite_files = Path("images/ghosts/clyde")

        frames = [
            arcade.load_texture(str(frame))
            for frame in sprite_files.iterdir()
        ]

        self.frames = {
            "down": frames[:2],
            "left": frames[2:4],
            "right": frames[4:6],
            "up": frames[6:]
        }

        self.textures = self.frames["down"]
        self.texture = self.textures[0]
        self.center_x = self.jail_center[0] + self.width + 15
        self.center_y = self.jail_center[1]
        self.jail_time = self.JAIL_TIME

        self.destination = [self.center_x, self.jail_center[1] - 12]



