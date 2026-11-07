import arcade
from pathlib import Path
from board.ghosts.ghost import Ghost
import random
from config import *

class Blinky(Ghost):

    
    #TODO: create a dictionary of attributes based on color of the ghost
    def __init__(self, jail_center):

        super().__init__(jail_center, sprite_files=Path("images/ghosts/blinky"))
        self.center_x = self.jail_center[0] 
        self.center_y = self.jail_center[1] + self.width + 20
        self.mode = self.Mode.CHASE
        self.destination = None


    def chase(self, pacman_pos):
        #check to see if a new path is needed
        if self.new_path:
            path = arcade.astar_calculate_path(
                start_point=self.position,
                end_point=pacman_pos,
                astar_barrier_list=self.barrier_list,
                diagonal_movement=False,
            ) 

            if  path:
                self.path = path
                self.path_index = 0
                self.destination = self.path[self.path_index]

            self.new_path = False
        
        #check to see if we've reached the next point on the path
        if self.position == self.destination:

            #if we've reached the end of the current path before getting a new one, reverse
            if self.path_index == len(self.path) - 1:
                self.path_index -= 1
                self.new_path = True
                self.move_timer = 0

            else:
                self.path_index += 1

            self.destination = self.path[self.path_index]

        direction = self.move()

        # check for needing a new path next time through or moving to scatter
        # if self.move_timer >= self.CHASE_TIME_TOTAL:
        #     self.mode = self.Mode.SCATTER
        #     self.move_timer = 0
        #     self.new_path = True

        if self.move_timer >= self.CHASE_TIME_ITER:
            self.move_timer = 0
            self.new_path = True


        return direction
