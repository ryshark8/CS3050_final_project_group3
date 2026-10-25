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
    "cherry": 100,
    "strawberry": 300,
    "orange": 500,
    "apple": 700,
    "melon": 1000,
    "galaxian": 2000,
    "bell": 3000,
    "key": 5000
}

# the sizes of each of the images, provided default does not look good
DEFAULT_FRUIT_SIZE = 20
FRUIT_SIZE = {
    "galaxian": 25,
    "bell": 18,
    "key": 15
}

# which fruit appears on what level, in order
LEVEL_FRUIT = [
     "cherry",
    "strawberry",
    "orange",
    "apple",
    "melon",
    "galaxian",
    "bell",
    "key",
]

def fruit_for_level(level):
    return LEVEL_FRUIT[min(level, len(LEVEL_FRUIT) - 1)]

class Fruit(arcade.Sprite):
    def __init__(self, kind, x, y, size=None):
        texture = arcade.load_texture(IMAGE_DIR / f"{kind}.png")
        super().__init__(texture, center_x=x, center_y=y)
        self.kind = kind
        self.points = FRUIT_POINTS[kind]

        # scale the fruits / objects
        if size is None:
            size = FRUIT_SIZE.get(kind, DEFAULT_FRUIT_SIZE)

        # fit it to one tile
        self.scale = size / texture.width
        self.time_left = FRUIT_LIFETIME

    def update(self, delta_time: float = 1 / 60, **kwargs):
        self.time_left -= delta_time
        if self.time_left <= 0:
            # get rid of it if it has not been eaten in FRUIT_LIFETIME
            self.remove_from_sprite_lists()