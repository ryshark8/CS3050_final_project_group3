import arcade
from pathlib import Path
from board.ghosts.ghost import Ghost
from config import *

class Blinky(Ghost):

    
    #TODO: create a dictionary of attributes based on color of the ghost
    def __init__(self, barrier_list):

        super().__init__(barrier_list)

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
        self.center_x = JAIL_CENTER[0] 
        self.center_y = JAIL_CENTER[1] + 40
        self.jail_time = 0
        self.jail = False

        self.destination = [400, 400]


    def chase(self, pacman_pos):

        if self.path == None:
            self.path = arcade.astar_calculate_path(
                start_point=self.position,
                end_point=pacman_pos,
                astar_barrier_list=self.barrier_list,
                diagonal_movement=False,
            )
            self.path_pos = 0
        self.destination = self.path[self.path_pos]

        #check to see if we've reached the next point on the path
        if self.position == self.destination:
            self.path_pos += 1
            self.destination = self.path[self.path_pos]

        x_diff = self.destination[0] - self.center_x
        y_diff = self.destination[1] - self.center_y

        #can only move orthogonally
        if x_diff:
            speed = min(self.speed, abs(x_diff))
            sign = (x_diff > 0) - (x_diff < 0)
            self.center_x += speed * sign
            direction = ('x', x_diff)

        elif y_diff:
            speed = min(self.speed, abs(y_diff))
            sign = (y_diff > 0) - (y_diff < 0)
            self.center_y += speed * sign
            direction = ('y', y_diff)


        return direction