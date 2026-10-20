"""
Pac-Man sprite
"""

import arcade
from config import *
from pathlib import Path

# some constants
MOVEMENT_SPEED = 5
RADIUS = 13
MOUTH_INTERVAL = 0.1
IMAGE_DIR = Path(__file__).parent / "images/pacman"


class Pacman(arcade.Sprite):
    def __init__(self, x, y):
        self.open_texture = arcade.load_texture(IMAGE_DIR / "right_frame1.png")
        self.closed_texture = arcade.load_texture(IMAGE_DIR / "right_frame2.png")
        super().__init__(self.open_texture, center_x=x, center_y=y)

        # scale the image so he is RADIUS * 2 pixels wide, whatever the file size
        self.scale = (RADIUS * 2) / self.open_texture.width

        self.mouth_timer = 0.0

    def update(self, delta_time: float = 1 / 60, **kwargs):
        # movement (change_x / change_y are built into Sprite)
        self.center_x += self.change_x
        self.center_y += self.change_y
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