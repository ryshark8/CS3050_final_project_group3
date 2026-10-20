from ghosts.blinky import Blinky
from ghosts.pinky import Pinky
from ghosts.inky import Inky
from ghosts.clyde import Clyde


"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade
from pacman import Pacman
from config import *

class GameView(arcade.View):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self):
        super().__init__()

        self.background_color = arcade.color.AMAZON

        self.ghost_list = arcade.SpriteList()
        self.ghost_list.extend([Inky(), Blinky(), Pinky(), Clyde()])
        
        # If you have sprite lists, you should create them here,
        # and set them to None
        self.sprites = None
        self.pacman = None
        self.reset()

    def reset(self):
        """Reset the game to the initial state."""
        # Do changes needed to restart the game here if you want to support that
        self.sprites = arcade.SpriteList()
        self.pacman = Pacman(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.sprites.append(self.pacman)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        
        self.clear()
        self.ghost_list.draw()
        self.sprites.draw()
        # Call draw() on all your sprite lists below
        

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.ghost_list.update()
        pass
        self.sprites.update(delta_time)

    def on_key_press(self, key, modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        self.pacman.key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        self.pacman.key_release(key, modifiers)


def main():
    """ Main function """
    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    # Create and setup the GameView
    game = GameView()

    # Show GameView on screen
    window.show_view(game)

    # Start the arcade game loop
    arcade.run()



if __name__ == "__main__":
    main()