"""this is the fruit class that draws them on the board"""

# some imports
import arcade
from pathlib import Path

# path to image folder
IMAGE_DIR = Path(__file__).parent / "../../images/fruits/"

# how long the fruit will stay on the board
FRUIT_LIFETIME = 10

# How many points each of the fruits is worth
# I only have cherry and dk what the other fruits are (sorry)
FRUIT_POINTS = {
    "cherries": 100
}

# which fruit appears on what level, in order
LEVEL_FRUIT = [
    "cherries"
]

def fruit_for_level(level):
    return LEVEL_FRUIT[min(level, len(LEVEL_FRUIT) - 1)]

class Fruit(arcade.Sprite):
    def __init__(self, kind, x, y, size=20):
        texture = arcade.load_texture(IMAGE_DIR / f"{kind}.png")
        super().__init__(texture, center_x=x, center_y=y)
        self.kind = kind
        self.points = FRUIT_POINTS[kind]

        # fit it to one tile
        self.scale = size / texture.width
        self.time_left = FRUIT_LIFETIME

    def update(self, delta_time: float = 1 / 60, **kwargs):
        self.time_left -= delta_time
        if self.time_left <= 0:
            # get rid of it if it has not been eaten in FRUIT_LIFETIME
            self.remove_from_sprite_lists()