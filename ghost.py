import arcade
from pathlib import Path

class Ghost(arcade.Sprite):
    """
    when intialized, should only need ghost color, the rest should be handled internally
    """

    FRAME_DURATION = 0.1
    
    #TODO: create a dictionary of attributes based on color of the ghost
    def __init__(self):
        super().__init__(self)

        sprite_files = Path("images/ghosts/blinky")

        self.textures = [
            arcade.load_texture(str(frame))
            for frame in sprite_files.iterdir()
        ]

        self.texture = self.textures[0]

        self.elapsed_time = 0
        self.center_x = 0
        self.center_y = 0
        self.scale = 3


    def update_animation(self, delta_time):
        self.cur_texture_index = (self.cur_texture_index + 1) % len(self.textures)
        self.texture = self.textures[self.cur_texture_index]

    def update(self, delta_time):
        self.elapsed_time += delta_time

        if self.elapsed_time >= self.FRAME_DURATION:
            self.update_animation(delta_time=delta_time)
            self.elapsed_time = 0

        


"""
JUST TO GET THINGS TO DISPLAY
"""

# Constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Platformer"

class GameView(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

        # Variable to hold our texture for our player
        # self.player_texture = arcade.load_texture(
        #     ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        # )

        # Separate variable that holds the player sprite
        self.player_sprite = Ghost()
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128

        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        pass

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Draw our sprites
        arcade.draw_sprite(self.player_sprite)

    def on_update(self, delta_time):
        self.player_sprite.update(delta_time=delta_time)

def main():
    """Main function"""
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()