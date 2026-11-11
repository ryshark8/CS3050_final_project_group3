"""Basic ghost functionality"""

import random
from enum import Enum
import arcade
from config import TILE_SIZE


class Ghost(arcade.Sprite):
    """
    Parent class for each individual ghost sprite
    """

    FRAME_DURATION = 0.5

    # currently hardcoding this but it may be a good idea going forward to get this via parameter
    # from Level because it will change
    CHASE_TIME_ITER = 4  # time between path recalculations when chasing pacman
    CHASE_TIME_TOTAL = 20
    SCATTER = [5, 5, 7, 7]

    """
    Mode represents state of the ghosts in the game which are triggered by different events.
    Each mode has an associated movement pattern and/or texture
    """

    class Mode(Enum):
        """Defining different movement patterns"""

        JAIL = "jail"
        CHASE = "chase"
        SCATTER = "scatter"
        SCARED = "scared"
        EATEN = "eaten"

    def __init__(self, jail_center, sprite_files):

        super().__init__()

        frames = [arcade.load_texture(str(frame)) for frame in sprite_files.iterdir()]

        self.frames = {
            "down": frames[:2],
            "left": frames[2:4],
            "right": frames[4:6],
            "up": frames[6:],
        }

        self.textures = self.frames["down"]
        self.texture = self.textures[0]
        self.size = (TILE_SIZE * 2, TILE_SIZE * 2)

        self.barrier_list = None

        self.elapsed_time = 0
        self.animation_timer = 0
        self.move_timer = 0
        self.speed = 2

        # for jail functionality
        self.jail_time = None
        self.jail_center = jail_center

        self.mode = self.Mode.JAIL

        self.destination = None
        self.path = None
        self.path_index = 0
        self.assigned_corner = {}
        self.new_path = True
        self.chase_timer = 0

    def update_animation(self, direction):
        """
        updating the ghost's animation
        """
        # make sure eyes are correct
        if direction[0] == "x":
            if direction[1] > 0:
                self.textures = self.frames["right"]
            else:
                self.textures = self.frames["left"]

        else:
            if direction[1] > 0:
                self.textures = self.frames["up"]
            else:
                self.textures = self.frames["down"]

        self.cur_texture_index = (self.cur_texture_index + 1) % len(self.textures)
        self.texture = self.textures[self.cur_texture_index]

    def update(self, delta_time, pacman_pos):
        """
        updating ghost position and animation
        """
        # movement logic
        match self.mode.value:

            case "jail":

                if self.elapsed_time >= self.jail_time:
                    self.mode = self.Mode.CHASE
                    return

                direction = self.jail(pacman_pos)

            case "chase":
                direction = self.chase(pacman_pos)

            case "scatter":
                direction = self.scatter()

            case "eaten":
                pass
            case "scared":
                pass

        # update the animation
        if self.animation_timer >= self.FRAME_DURATION:
            self.update_animation(direction=direction)
            self.animation_timer = 0

        self.move_timer += delta_time
        self.elapsed_time += delta_time
        self.animation_timer += delta_time

    def jail(self, pacman_pos):
        """
        dictates movement for when ghosts are in jail
        """
        if self.center_y == self.destination[1]:
            # go down
            if self.center_y > self.jail_center[1]:
                self.destination[1] = self.jail_center[1] - 6

            else:
                self.destination[1] = self.jail_center[1] + 6

        distance = self.destination[1] - self.center_y
        speed = min(self.speed, abs(distance))
        sign = (distance > 0) - (distance < 0)
        self.center_y += speed * sign

        # to help avoid not having a path once chasing starts
        if self.path is None and self.elapsed_time >= self.jail_time // 2:
            self.path = arcade.astar_calculate_path(
                start_point=self.position,
                end_point=pacman_pos,
                astar_barrier_list=self.barrier_list,
                diagonal_movement=False,
            )

        return ("y", distance)

    def chase(self, pacman_pos):
        on_node = self.destination is None or tuple(self.position) == tuple(self.destination)

        if on_node:
            target = (round(pacman_pos[0] / TILE_SIZE) * TILE_SIZE,
                      round(pacman_pos[1] / TILE_SIZE) * TILE_SIZE)

            path = arcade.astar_calculate_path(
                start_point=self.position,
                end_point=target,   # make the target NOT pacmans position
                astar_barrier_list=self.barrier_list,
                diagonal_movement=False,
            )
            if path:
                standing = tuple(path[0]) == tuple(self.position)
                self.destination = path[1] if standing and len(path) > 1 else path[0]

        return self.move()

    def scatter(self):
        """
        function that dictates movement for "scatter mode" i.e when ghosts are returning to
        their own corners briefly in between chase sessions
        """
        if self.new_path:
            x = random.randint(
                self.assigned_corner["left"], self.assigned_corner["right"]
            )
            y = random.randint(
                self.assigned_corner["bottom"], self.assigned_corner["top"]
            )
            self.path = arcade.astar_calculate_path(
                start_point=self.position,
                end_point=(x, y),
                astar_barrier_list=self.barrier_list,
                diagonal_movement=False,
            )
            self.chase_timer = 0
            self.path_index = 0
            self.new_path = False

        self.destination = self.path[self.path_index]

        # check to see if we've reached the next point on the path
        if self.position == self.destination:
            self.path_index += 1
            self.destination = self.path[self.path_index]

        direction = self.move()

        # check to see if we should go back to chasing yet
        if self.move_timer >= self.SCATTER[1]:
            self.mode = self.Mode.CHASE
            self.move_timer = 0
            self.new_path = True

        elif self.position == self.path[-1]:
            self.new_path = True

        return direction

    def scared(self):
        """movement for scared ghosts"""
        return

    def eaten(self):
        """movement for eaten ghosts"""
        return

    def move(self):
        """General orthogonal movement function"""

        direction = ("x", 0)
        if self.destination is not None:

            x_diff = self.destination[0] - self.center_x
            y_diff = self.destination[1] - self.center_y

            # can only move orthogonally
            if x_diff:
                speed = min(self.speed, abs(x_diff))
                sign = (x_diff > 0) - (x_diff < 0)
                self.center_x += speed * sign
                direction = ("x", x_diff)

            elif y_diff:
                speed = min(self.speed, abs(y_diff))
                sign = (y_diff > 0) - (y_diff < 0)
                self.center_y += speed * sign
                direction = ("y", y_diff)

        return direction
