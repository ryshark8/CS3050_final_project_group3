import arcade
from pathlib import Path
from board.ghosts.ghost import Ghost
import random
from config import *


class Inky(Ghost):

    JAIL_TIME = 6
    CHASE_TIME_ITER = 2 # time between path recalculations when chasing pacman
    CHASE_TIME_TOTAL = 20

    def __init__(self, jail_center, board_rows, board_cols):

        super().__init__(jail_center, sprite_files=Path("images/ghosts/inky"))

    
        self.center_x = self.jail_center[0] - (self.width + 15)
        self.center_y = self.jail_center[1]
        self.jail_time = self.JAIL_TIME
        

        self.destination = [self.center_x, self.jail_center[1] - 12]

        # calculating the assigned corner, Inky's is bottom right
        self.assigned_corner = {
            "top": board_rows * TILE_SIZE,
            "bottom": int((board_rows / 2) * TILE_SIZE),
            "left": int((board_cols / 2) * TILE_SIZE),
            "right": board_cols * TILE_SIZE,
        }

    def chase(self, pacman_pos):

        #check to see if a new path is needed NOTE: scatter always happens first so there is no case where path is empty
        if self.new_path:
            self.path = arcade.astar_calculate_path(
                start_point=self.position,
                end_point=pacman_pos,
                astar_barrier_list=self.barrier_list,
                diagonal_movement=False,
            )
            self.path_index = 0
            self.new_path = False
            
        self.destination = self.path[self.path_index]

        #check to see if we've reached the next point on the path
        if self.position == self.destination:
            self.path_index += 1
            self.destination = self.path[self.path_index]

        direction = self.move()

        # check for needing a new path next time through or moving to scatter
        if self.move_timer >= self.CHASE_TIME_TOTAL:
            self.mode = self.Mode.SCATTER
            self.move_timer = 0
            self.new_path = True

        if self.chase_timer >= self.CHASE_TIME_ITER or self.position == self.path[-1]:
            self.new_path = True


        return direction
