import arcade
from pathlib import Path
from board.ghosts.ghost import Ghost
from config import *

class Pinky(Ghost):

    JAIL_TIME = 10
    
    #TODO: create a dictionary of attributes based on color of the ghost
    def __init__(self, barrier_list):

        super().__init__(barrier_list)

        sprite_files = Path("images/ghosts/pinky")

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
        self.center_y = JAIL_CENTER[1]
        self.jail_time = self.JAIL_TIME

        self.destination = [self.center_x, JAIL_CENTER[1] + 6]


    # def update():
    #     pass
        

    # def update_animation(self, direction):

    #     # make sure eyes are correct
    #     if direction[0] == 'x':
    #         if direction[1] > 0:
    #             self.textures = self.frames['right']
    #         else:
    #             self.textures = self.frames['left']

    #     else:
    #         if direction[1] > 0:
    #             self.textures = self.frames['up']
    #         else:
    #             self.textures = self.frames['down']

    #     self.cur_texture_index = (self.cur_texture_index + 1) % len(self.textures)
    #     self.texture = self.textures[self.cur_texture_index]

    # def update(self, delta_time):

    #     # movement logic
    #     start_x = self.center_x
    #     start_y = self.center_y

    #     self.dest_x = 500
    #     self.dest_y = 400

    #     x_diff = self.dest_x - start_x
    #     y_diff = self.dest_y - start_y

    #     #can only move orthogonally
    #     if x_diff:
    #         speed = min(self.speed, x_diff)
    #         self.center_x += speed
    #         direction = ('x', x_diff)
    #     elif y_diff:
    #         speed = min(self.speed, y_diff)
    #         self.center_y += speed
    #         direction = ('y', y_diff)
        
    #     #update the animation
    #     if self.animation_timer >= self.FRAME_DURATION:
    #         self.update_animation(delta_time=delta_time, direction=direction)
    #         self.animation_timer = 0


    #     self.elapsed_time += delta_time
    #     self.animation_timer += delta_time

        

        
