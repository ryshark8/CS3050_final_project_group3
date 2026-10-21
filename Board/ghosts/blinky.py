import arcade
from pathlib import Path
from Board.ghosts.ghost import Ghost
import random

class Blinky(Ghost):

    
    #TODO: create a dictionary of attributes based on color of the ghost
    def __init__(self):

        super().__init__()

        sprite_files = Path("images/ghosts/blinky")

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
        self.center_x = random.randint(0, 1280)
        self.center_y = random.randint(0, 720)

