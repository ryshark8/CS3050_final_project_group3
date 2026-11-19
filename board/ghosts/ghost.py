"""Basic ghost functionality"""

import random
from enum import Enum
from collections import deque
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

    REPATH_COOLDOWN = 0.25

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
        self._blocked = None # caching a set of cells that are blocked

        self.elapsed_time = 0
        self.animation_timer = 0
        self.move_timer = 0
        self.speed = 2

        self.repath_cooldown = 0

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
                    # clear the jail movement state, was fucking up path finding
                    # I think lol
                    self.destination = None
                    self.path = None
                    self.path_index = 0
                    self.new_path = True
                    self.move_timer = 0
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
        self.repath_cooldown -= delta_time

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


        return ("y", distance)

    # ------------- path finding helpers  --------------------

    def blocked_cells(self):
        if self._blocked is None:
            self._blocked = set(self.barrier_list.barrier_list)
        return self._blocked

    def in_bounds(self, cell):
        """Wether a cell is in bounds or in the barrier list"""
        bl = self.barrier_list
        return bl.left <= cell[0] <= bl.right and bl.bottom <= cell[1] <= bl.top

    def snap_to_open_cell(self, pos, max_radius=2):
        """
        return the nearest cell in grid units that is not a wall
        or None, have to do this to stop the jitter that was happening when A*
        failed
        """
        gs = self.barrier_list.grid_size
        blocked = self.blocked_cells()

        cx, cy = round(pos[0] / gs), round(pos[1] / gs)
        best, best_dist = None, float("inf")
        for dx in range(-max_radius, max_radius + 1):
            for dy in range(-max_radius, max_radius + 1):
                cell = (cx + dx, cy + dy)
                if cell in blocked or not self.in_bounds(cell):
                    continue
                dist = abs(cell[0] * gs - pos[0]) + abs(cell[1] * gs - pos[1])
                if dist < best_dist:
                    best, best_dist = cell, dist
        return best

    def find_path(self, start_pos, end_pos):
        """
        I have just done BFS for a video game :/
        """
        gs = self.barrier_list.grid_size

        start = self.snap_to_open_cell(start_pos)
        if start is None:
            return None

        # CHANGED: the raw target cell, used for "closest reachable cell"
        # if the snapped target is missing or unreachable
        target = (round(end_pos[0] / gs), round(end_pos[1] / gs))
        end = self.snap_to_open_cell(end_pos)

        blocked = self.blocked_cells()
        came_from = {start: None}
        queue = deque([start])

        # track the cell nearest the target as we go
        def dist_to_target(c):
            return abs(c[0] - target[0]) + abs(c[1] - target[1])

        closest = start
        closest_dist = dist_to_target(start)

        while queue:
            current = queue.popleft()
            if current == end:
                break

            d = dist_to_target(current)
            if d < closest_dist:
                closest, closest_dist = current, d

            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nxt = (current[0] + dx, current[1] + dy)
                if nxt in came_from or nxt in blocked or not self.in_bounds(nxt):
                    continue
                came_from[nxt] = current
                queue.append(nxt)

        # Fall back to the closest reachable cell.
        if end is None or end not in came_from:
            end = closest

        path = []
        cell = end
        while cell is not None:
            path.append((cell[0] * gs, cell[1] * gs))
            cell = came_from[cell]
        path.reverse()
        return path

    def set_path(self, path):
        """start following the new path"""
        self.path = path
        self.path_index = 0
        self.destination = path[0]

    def follow_path(self):
        """ Move on the current path """
        if self.path is None:
            return ("x", 0)

        if self.position == self.destination:
            if self.path_index < len( self.path) - 1:
                self.path_index += 1
                self.destination = self.path[self.path_index]
            else:
                self.new_path = True

        return self.move()


    def can_repath(self):
        """
        True if this ghost is allowed to run find_path this frame
        doing this because I was calling it too often, making the
        frames slow down a ton
        """
        return self.new_path and self.repath_cooldown <= 0


# ------------- movement -------------------

    def chase(self, pacman_pos):
        # check to see if we need new path
        if self.can_repath():
            self.repath_cooldown = self.REPATH_COOLDOWN
            path = self.find_path(self.position, pacman_pos)

            # if find_path returns None keep the old path
            # and continure to follow it
            if path:
                self.set_path(path)

            self.new_path = False

        direction = self.follow_path()

        if self.move_timer >= self.CHASE_TIME_ITER:
            self.move_timer = 0
            self.new_path = True

        return direction

    def scatter(self):
        """
        "scatter mode" i.e when ghosts are returning to
        their own corners briefly in between chase sessions
        """
        if self.can_repath():
            self.repath_cooldown = self.REPATH_COOLDOWN
            x = random.randint(
                self.assigned_corner["left"], self.assigned_corner["right"]
            )
            y = random.randint(
                self.assigned_corner["bottom"], self.assigned_corner["top"]
            )
            path = self.find_path(self.position, (x,y))

            if path:
                self.set_path(path)
                self.new_path = False
            # else here would be when it is in a wall

            self.chase_timer = 0

        direction = self.follow_path()

        # check if we should go back to chasing yet
        if self.move_timer >= self.SCATTER[1]:
            self.mode = self.Mode.CHASE
            self.move_timer = 0
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
