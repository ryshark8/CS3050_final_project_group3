import arcade
import random
from config import *

class Ghost(arcade.Sprite):
    """
    when intialized, should only need ghost color, the rest should be handled internally
    """

    FRAME_DURATION = 0.2
    
    #TODO: create a dictionary of attributes based on color of the ghost
    def __init__(self, barrier_list):
        super().__init__(self)

        self.barrier_list = barrier_list

        self.elapsed_time = 0
        self.scale = 1.5
        self.animation_timer = 0
        self.found = False
        self.speed = 1 

        # for jail functionality
        self.jail_time = None
        self.jail = True

        self.destination = None
        self.path = None
        self.path_pos = 0
        


    def update_animation(self, direction):
        # make sure eyes are correct
        if direction[0] == 'x':
            if direction[1] > 0:
                self.textures = self.frames['right']
            else:
                self.textures = self.frames['left']

        else:
            if direction[1] > 0:
                self.textures = self.frames['up']
            else:
                self.textures = self.frames['down']

        self.cur_texture_index = (self.cur_texture_index + 1) % len(self.textures)
        self.texture = self.textures[self.cur_texture_index]

    def update(self, delta_time, pacman_pos):
        # movement logic
        

        # jailed ghosts only move up and down
        if self.jail:
            # if self.elapsed_time >= self.jail_time:
            #     self.jail = False

            direction = self.jail_movement(self)
            self.update_animation(direction=direction)
            self.elapsed_time += delta_time
            return

        
        #get new end point
        #direction = self.chase(pacman_pos)
        direction = ("x", 0)
        
        #update the animation
        if self.animation_timer >= self.FRAME_DURATION:
            self.update_animation(direction=direction)
            self.animation_timer = 0


        self.elapsed_time += delta_time
        self.animation_timer += delta_time


    #TODO: create logic for scared ghost movement
    def scared(self):
        pass

    @staticmethod
    def jail_movement(self):

        if self.center_y == self.destination[1]:
            #go down
            if self.center_y > JAIL_CENTER[1]:
                self.destination[1] = JAIL_CENTER[1] - 6

            else:
                self.destination[1] = JAIL_CENTER[1] + 6

        distance = self.destination[1] - self.center_y
        speed = min(self.speed, abs(distance))
        sign = (distance > 0) - (distance < 0)
        self.center_y += speed * sign
        
        return ('y', distance)

    def chase(self, pacman_pos):
        pass