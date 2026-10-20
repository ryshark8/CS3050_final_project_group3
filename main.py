"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade

import level1_board
import pacman_board

WINDOW_WIDTH = 550
WINDOW_HEIGHT = 700
WINDOW_TITLE = "PACMAN"

TILE_SIZE = 15
LABEL_SIZE = 14
SCORE_SIZE = 12
LABEL_POSITION = 32
SCORE_POSITION = 50
HIGH_SCORE_POSITION = 12

# Window Configuration
MARGIN = 20
HEADER_HEIGHT = 55 # For score section


class Level:
    def __init__(self, tile_size, label_size, score_size, label_position, score_position,
                 high_score_position, margin, header_height, rows, cols, maze,
                 screen_width, screen_height, board_width, board_height):

        self.wall_list = arcade.SpriteList()

        self.tile_size = tile_size
        self.label_size = label_size
        self.score_size = score_size
        self.label_position = label_position
        self.score_position = score_position
        self.high_score_position = high_score_position
        self.margin = margin
        self.header_height = header_height
        self.rows = rows
        self.cols = cols
        self.maze = maze
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.board_width = board_width
        self.board_height = board_height

def setup_level1():
    level1 = Level(TILE_SIZE, LABEL_SIZE, SCORE_SIZE, LABEL_POSITION, SCORE_POSITION,
                   HIGH_SCORE_POSITION, MARGIN, HEADER_HEIGHT, level1_board.rows, level1_board.cols,
                   level1_board.maze, level1_board.screen_width, level1_board.screen_height,
                   level1_board.board_width, level1_board.board_height)

    level1.board = pacman_board.PacmanBoard(level1)

    level1.wall_list = level1.board.wall_list

    return level1


class GameView(arcade.View):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self):
        super().__init__()

        self.background_color = (5, 5, 12)

        # If you have sprite lists, you should create them here,
        # and set them to None
        self.levels = None
        self.current_level = None
        self.wall_list = None

    def setup(self):
        self.levels = []

        level = setup_level1()
        self.levels.append(level)

        self.current_level = 0

        self.wall_list = level.wall_list

    def reset(self):
        """Reset the game to the initial state."""
        # Do changes needed to restart the game here if you want to support that
        pass

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()

        # Call draw() on all your sprite lists below
        level = self.levels[self.current_level]
        level.board.draw_maze()
        level.board.draw_header()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        pass

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        pass

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    """ Main function """

    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    # Create and setup the GameView
    game = GameView()

    game.setup()

    # Show GameView on screen
    window.show_view(game)

    # Start the arcade game loop
    arcade.run()



if __name__ == "__main__":
    main()