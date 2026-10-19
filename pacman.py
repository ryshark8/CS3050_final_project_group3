"""
This is the file that I am working in to get pac man on a board and moving around
"""

# some imports
import arcade

# some constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Pacman"
MOVEMENT_SPEED = 5
RADIUS = 30
MOUTH_INTERVAL = 0.10 # seconds

class Pacman(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK)

        self.x = 300
        self.y = 300
        self.change_x = 0
        self.change_y = 0
        self.tilt = 0

        # mouth animation
        self.start_angle = 45
        self.end_angle = 315
        self.mouth_timer = 0.0

    def on_draw(self):
        """Called when we draw something, well everything"""
        self.clear()
        # this is code (mostly) taken from here
        # https://api.arcade.academy/en/3.3.3/api_docs/api/drawing_primitives.html
        # it is what draws pacman
        arcade.draw_arc_filled(
            center_x=self.x,
            center_y=self.y,
            width=RADIUS * 2,
            height=RADIUS * 2,
            color=arcade.color.YELLOW,
            start_angle=self.start_angle,
            end_angle=self.end_angle,
            tilt_angle=self.tilt,
            num_segments=128
        )

    def on_key_press(self, key, modifiers):
        """called when a key is pressed"""
        if key == arcade.key.UP:
            self.change_y = MOVEMENT_SPEED
            self.tilt = 270
        elif key == arcade.key.DOWN:
            self.change_y = -MOVEMENT_SPEED
            self.tilt = 90
        elif key == arcade.key.LEFT:
            self.change_x = -MOVEMENT_SPEED
            self.tilt = 180
        elif key == arcade.key.RIGHT:
            self.change_x = MOVEMENT_SPEED
            self.tilt = 0

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        if key in (arcade.key.UP, arcade.key.DOWN):
            self.change_y = 0
        elif key in (arcade.key.LEFT, arcade.key.RIGHT):
            self.change_x = 0

    def on_update(self, delta_time):
        """
        Move pacman and keep him on the screen
        This runs about 60 times a second, so any animation
        not using a timer will just flicker, see mouth movement
        """
        self.x += self.change_x
        self.y += self.change_y
        self.x = max(RADIUS, min(SCREEN_WIDTH - RADIUS, self.x))
        self.y = max(RADIUS, min(SCREEN_HEIGHT - RADIUS, self.y))

        # animate the movement of his mouth
        if self.change_x or self.change_y:
            self.mouth_timer += delta_time
            if self.mouth_timer >= MOUTH_INTERVAL:
                if self.start_angle == 45:
                    self.start_angle = 0
                    self.end_angle = 360
                else:
                    self.start_angle = 45
                    self.end_angle = 315

def pacman():
    Pacman(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()

pacman()