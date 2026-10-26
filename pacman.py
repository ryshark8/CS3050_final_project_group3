"""
Pac-Man sprite
"""

import arcade
from config import *
from pathlib import Path

# some constants
MOVEMENT_SPEED = 2
RADIUS = 9
DEATH_FRAME_DURATION = 0.12
MOUTH_INTERVAL = 0.1
IMAGE_DIR = Path(__file__).parent / "images/pacman"

# some more constants, these ones set the keys
KEY_TO_DIR = {
    arcade.key.UP: (0, 1, 270),
    arcade.key.DOWN: (0, -1, 90),
    arcade.key.LEFT: (-1, 0, 180),
    arcade.key.RIGHT: (1, 0, 0),
}

# how many px off from a corridor that he will still take
CORNER_SLACK = 6

class Pacman(arcade.Sprite):
    def __init__(self, x, y):
        # movement
        self.open_texture = arcade.load_texture(IMAGE_DIR / "right_frame1.png")
        self.closed_texture = arcade.load_texture(IMAGE_DIR / "right_frame2.png")

        # death: there is certainly a better way to do this
        self.death_textures = [
            arcade.load_texture(IMAGE_DIR / "death_frame0.png"),
            arcade.load_texture(IMAGE_DIR / "death_frame1.png"),
            arcade.load_texture(IMAGE_DIR / "death_frame2.png"),
            arcade.load_texture(IMAGE_DIR / "death_frame3.png"),
            arcade.load_texture(IMAGE_DIR / "death_frame4.png"),
            arcade.load_texture(IMAGE_DIR / "death_frame5.png"),
            arcade.load_texture(IMAGE_DIR / "death_frame6.png"),
            arcade.load_texture(IMAGE_DIR / "death_frame7.png"),
            arcade.load_texture(IMAGE_DIR / "death_frame8.png"),
            arcade.load_texture(IMAGE_DIR / "death_frame9.png"),
            arcade.load_texture(IMAGE_DIR / "death_frame10.png"),
            arcade.load_texture(IMAGE_DIR / "death_frame11.png"),
            arcade.load_texture(IMAGE_DIR / "death_frame12.png"),
            arcade.load_texture(IMAGE_DIR / "death_frame13.png"),
            arcade.load_texture(IMAGE_DIR / "death_frame14.png"),
            arcade.load_texture(IMAGE_DIR / "death_frame15.png")
        ]

        super().__init__(self.open_texture, center_x=x, center_y=y)

        # some game specific attributes
        self.lives = 3
        self.is_dying = False
        self.is_dead = False

        # coords for where to spawn pacman, right below the ghost prison or whatever
        self.spawn_x = 250
        self.spawn_y = 260

        # death attributes
        self.death_frame = 0
        self.death_timer = 0.0

        # movement variables
        self.walls = None
        self.direction = (0, 0, 0)
        self.next_direction = (0, 0, 0)
        self._last_pos = (x, y)

        # scale the image so he is RADIUS * 2 pixels wide, whatever the file size
        self.scale = (RADIUS * 2) / self.open_texture.width

        self.mouth_timer = 0.0

    def start_death_animation(self):
        self.is_dead = False
        self.death_frame = 0
        self.death_timer = 0.0
        self.angle = 0
        self.texture = self.death_textures[0]

    def update_death(self, delta_time):
        self.death_timer += delta_time
        if self.death_timer >= DEATH_FRAME_DURATION:
            self.death_timer = 0.0
            self.death_frame += 1
            if self.death_frame >= len(self.death_textures):
                self.is_dead = True
            else:
                self.texture = self.death_textures[self.death_frame]

    def respawn(self):
        """ Respawn pacman if he has died """
        self.center_x = self.spawn_x
        self.center_y = self.spawn_y
        self.change_x = self.change_y = 0
        self.angle = 0
        self.texture = self.open_texture
        self.mouth_timer = 0.0

        # reset the movement vars
        self.direction = (0, 0, 0)
        self.next_direction = (0, 0, 0)

    def loose_life(self):
        if self.is_dying: return # death has been kicked off can't kill him again
        self.is_dying = True

        # make sure he can't move cuz hes dead yk
        self.change_x = 0
        self.change_y = 0

        self.start_death_animation()

    def kill_pacman(self):
        self.is_dying = False
        self.lives -= 1
        if self.lives > 0:
            self.respawn()

    # this is the one that makes him move prettier
    # like he ends up in the lane instead of smashing his head into the corner
    def _try_turn(self, direction):
        """Turn if possible, nudging him sideways a few px to line up with the opening."""
        dx, dy, _ = direction
        if not self._blocked(dx, dy):
            return True

        for offset in range(1, CORNER_SLACK + 1):
            for sign in (1, -1):
                ox = sign * offset if dy != 0 else 0   # turning vertical -> nudge in x
                oy = sign * offset if dx != 0 else 0   # turning horizontal -> nudge in y
                self.center_x += ox
                self.center_y += oy
                # the nudged spot must be clear, and the new direction must be open from it
                if not self._blocked(0, 0) and not self._blocked(dx, dy):
                    return True
                self.center_x -= ox
                self.center_y -= oy
        return False

    def _set_direction(self, direction):
        dx, dy, angle = direction
        self.direction = direction
        self.change_x = dx * MOVEMENT_SPEED
        self.change_y = dy * MOVEMENT_SPEED
        self.angle = angle

    def _blocked(self, dx, dy):
        """True if moving one step in (dx, dy) would hit a wall."""
        if self.walls is None:
            return False
        old_x, old_y = self.center_x, self.center_y
        self.center_x += dx * MOVEMENT_SPEED
        self.center_y += dy * MOVEMENT_SPEED
        hit = arcade.check_for_collision_with_list(self, self.walls)
        self.center_x, self.center_y = old_x, old_y
        return len(hit) > 0


    def update(self, delta_time: float = 1 / 60, **kwargs):
        self.center_x = max(RADIUS, min(WINDOW_WIDTH - RADIUS, self.center_x))
        self.center_y = max(RADIUS, min(WINDOW_HEIGHT - RADIUS, self.center_y))

        # make his turns look better
        nx, ny, _ = self.next_direction
        if (nx, ny) != (0, 0) and self._try_turn(self.next_direction):
            self._set_direction(self.next_direction)

        # mouth animation
        moving = (self.center_x, self.center_y) != self._last_pos
        self._last_pos = (self.center_x, self.center_y)
        if moving:
            self.mouth_timer += delta_time
            if self.mouth_timer >= MOUTH_INTERVAL:
                self.mouth_timer = 0.0
                self.texture = (self.closed_texture
                                if self.texture is self.open_texture
                                else self.open_texture)

    def on_key_press(self, key, modifiers):
        if key in KEY_TO_DIR:
            self.next_direction = KEY_TO_DIR[key]

    def on_key_release(self, key, modifiers):
        pass
