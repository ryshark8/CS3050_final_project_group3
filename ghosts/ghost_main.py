import arcade
from pathlib import Path
from blinky import Blinky
from pinky import Pinky
from inky import Inky
from clyde import Clyde

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

        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        self.ghost_list = arcade.SpriteList()
        self.ghost_list.extend([Inky(), Blinky(), Pinky(), Clyde()])
        pass

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Draw our sprites
        self.ghost_list.draw()

    def on_update(self, delta_time):
        self.ghost_list.update(delta_time=delta_time)


def main():
    """Main function"""
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
