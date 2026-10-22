"""
Pac-Man sprite
"""

import arcade
from config import *
from pathlib import Path

# some constants
MOVEMENT_SPEED = 2
RADIUS = 10
DEATH_FRAME_DURATION = 0.12
MOUTH_INTERVAL = 0.1
IMAGE_DIR = Path(__file__).parent / "images/pacman"


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
        self.spawn_x = 275
        self.spawn_y = 290

        # death attributes
        self.death_frame = 0
        self.death_timer = 0.0

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


    def update(self, delta_time: float = 1 / 60, **kwargs):
        self.center_x = max(RADIUS, min(WINDOW_WIDTH - RADIUS, self.center_x))
        self.center_y = max(RADIUS, min(WINDOW_HEIGHT - RADIUS, self.center_y))

        # mouth animation
        if self.change_x or self.change_y:
            self.mouth_timer += delta_time
            if self.mouth_timer >= MOUTH_INTERVAL:
                self.mouth_timer = 0.0
                if self.texture is self.open_texture:
                    self.texture = self.closed_texture
                else:
                    self.texture = self.open_texture

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.change_y = MOVEMENT_SPEED
            self.angle = 270
        elif key == arcade.key.DOWN:
            self.change_y = -MOVEMENT_SPEED
            self.angle = 90
        elif key == arcade.key.LEFT:
            self.change_x = -MOVEMENT_SPEED
            self.angle = 180
        elif key == arcade.key.RIGHT:
            self.change_x = MOVEMENT_SPEED
            self.angle = 0

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.UP, arcade.key.DOWN):
            self.change_y = 0
        elif key in (arcade.key.LEFT, arcade.key.RIGHT):
            self.change_x = 0