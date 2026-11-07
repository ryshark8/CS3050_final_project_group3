import arcade
from pathlib import Path
from board.ghosts.ghost import Ghost
from config import *

class Pinky(Ghost):

    JAIL_TIME = 10
    
    #TODO: create a dictionary of attributes based on color of the ghost
    def __init__(self, jail_center, board_rows, board_cols):

        super().__init__(jail_center, sprite_files=Path("images/ghosts/pinky"))

        self.texture = self.textures[0]
        self.center_x = self.jail_center[0]
        self.center_y = self.jail_center[1]
        self.jail_time = self.JAIL_TIME

        self.destination = [self.center_x, self.jail_center[1] + 12]


    # def chase(self, pacman_pos):
        
    #     #check to see if a new path is needed NOTE: scatter always happens first so there is no case where path is empty
    #     if self.new_path:
    #         path = arcade.astar_calculate_path(
    #             start_point=self.position,
    #             end_point=pacman_pos,
    #             astar_barrier_list=self.barrier_list,
    #             diagonal_movement=False,
    #         ) 

    #         if  path:
    #             self.path = path
    #             self.path_index = 0
                
    #         self.new_path = False
            
    #     self.destination = self.path[self.path_index]
          

    #     #check to see if we've reached the next point on the path
    #     if self.position == self.destination:
    #         self.path_index += 1

    #         if self.path_index == len(self.path):
    #             self.new_path = True
    #             self.move_timer = 0

    #         else:
    #             self.destination = self.path[self.path_index]

    #     direction = self.move()

    #     # check for needing a new path next time through or moving to scatter
    #     # if self.move_timer >= self.CHASE_TIME_TOTAL:
    #     #     self.mode = self.Mode.SCATTER
    #     #     self.move_timer = 0
    #     #     self.new_path = True

    #     if self.move_timer >= self.CHASE_TIME_ITER or self.position == self.path[-1]:
    #         self.move_timer = 0
    #         self.new_path = True



    #     return direction
    