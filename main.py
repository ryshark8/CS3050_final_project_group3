import arcade

from config import *
from game_logic import GameView


def main():
    """Main function"""

    # Create First Level and Window dimensions

    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    # Create and set up the GameView
    game = GameView()

    game.display_start_screen(window)

    # Start the arcade game loop
    arcade.run()


if __name__ == "__main__":
    main()
