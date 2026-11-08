"""Orange ghost"""

from pathlib import Path
from board.ghosts.ghost import Ghost


class Clyde(Ghost):
    """class for orange ghost"""

    JAIL_TIME = 15

    def __init__(self, jail_center, board_rows, board_cols):

        super().__init__(jail_center, sprite_files=Path("images/ghosts/clyde"))

        self.center_x = self.jail_center[0] + self.width + 15
        self.center_y = self.jail_center[1]
        self.jail_time = self.JAIL_TIME

        self.destination = [self.center_x, self.jail_center[1] - 12]

    # def chase(self, pacman_pos):

    #     if self.path == None:
    #         self.path = arcade.astar_calculate_path(
    #             start_point=self.position,
    #             end_point=pacman_pos,
    #             astar_barrier_list=self.barrier_list,
    #             diagonal_movement=False,
    #         )
    #     print(self.path)
    #     self.destination = self.path[self.path_pos]

    #     #check to see if we've reached the next point on the path
    #     if self.position == self.destination:
    #         self.path_pos += 1
    #         self.destination = self.path[self.path_pos]

    #     x_diff = self.destination[0] - self.center_x
    #     y_diff = self.destination[1] - self.center_y

    #     #can only move orthogonally
    #     if x_diff:
    #         speed = min(self.speed, abs(x_diff))
    #         sign = (x_diff > 0) - (x_diff < 0)
    #         self.center_x += speed * sign
    #         direction = ('x', x_diff)

    #     elif y_diff:
    #         speed = min(self.speed, abs(y_diff))
    #         sign = (y_diff > 0) - (y_diff < 0)
    #         self.center_y += speed * sign
    #         direction = ('y', y_diff)

    #     return direction
