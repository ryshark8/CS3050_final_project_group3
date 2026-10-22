import arcade

from board.levels import level1_board
from config import *
from board.levels.level1_board import *
from board.levels.level import *
from game_logic import GameView

def main():
    """Main function"""

    # Create First Level and Window dimensions
    level = Level(level1_board.maze)

    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(level.screen_width, level.screen_height, WINDOW_TITLE)

    # Create and set up the GameView
    game = GameView(level)

    game.setup()

    # Show GameView on screen
    window.show_view(game)

    # Start the arcade game loop
    arcade.run()


if __name__ == "__main__":
    main()