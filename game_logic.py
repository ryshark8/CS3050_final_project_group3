"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""

# some module imports
import arcade

# some file imports
from config import *
from board import pacman_board
from pacman import Pacman

from board.ghosts.blinky import Blinky
from board.ghosts.pinky import Pinky
from board.ghosts.inky import Inky
from board.ghosts.clyde import Clyde

class GameView(arcade.View):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, level):
        super().__init__()

        self.level = level

        self.background_color = (5, 5, 12)

        # If you have sprite lists, you should create them here,
        # and set them to None

        # set class lists to none
        self.sprites = None
        self.board = None
        self.pacman = None
        self.ghost_list = None

        self.physics_engine = None
        self.ghost_engines = None
        self.pacman_walls = None
        self.barrier_list = None

        self.current_score_label = None
        self.current_score = None

        self.levels = [self.level]
        self.current_level = 0

        self.reset()

    def setup(self):

        level = self.levels[self.current_level]

        self.board = pacman_board.PacmanBoard(level)

        self.wall_list = self.board.wall_list
        self.ghost_wall_list = self.board.ghost_wall_list

        # sprites
        # pacman
        self.sprites = arcade.SpriteList()

        # coords for where to spawn pacman, right below the ghost prison or whatever
        spawn_x = 275
        spawn_y = 290

        self.pacman = Pacman(spawn_x, spawn_y)
        self.sprites.append(self.pacman)

        # call the physics engine for collisions
        self.pacman_walls = arcade.SpriteList()
        self.pacman_walls.extend(self.wall_list)
        self.pacman_walls.extend(self.ghost_wall_list)

        barrier_list = arcade.AStarBarrierList(
            moving_sprite=self.pacman,
            blocking_sprites=self.wall_list,
            grid_size=TILE_SIZE,
            left=MARGIN,
            right=MARGIN + BOARD_WIDTH,
            bottom=MARGIN,
            top=MARGIN + BOARD_HEIGHT,
        )

        self.ghost_list = arcade.SpriteList()
        self.ghost_list.extend(
            [
                #Inky(barrier_list),
                Blinky(barrier_list),
                # Pinky(barrier_list),
                # Clyde(barrier_list),
            ]
        )

        # engine for pacman
        self.physics_engine = arcade.PhysicsEngineSimple(self.pacman, self.pacman_walls)

        # one engine for each of the ghost
        self.ghost_engines = [
            arcade.PhysicsEngineSimple(ghost, self.wall_list)
            for ghost in self.ghost_list
        ]

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


        # Call draw() on all your sprite lists below
        self.clear()

        # Call draw() on all your sprite lists below
        level = self.levels[self.current_level]
        self.board.draw()

        # draw the sprites
        self.ghost_list.draw()
        self.sprites.draw()

    # handle what happens when ghost and pacman collide
    def handle_ghost_colision(self, ghost_list):
        for ghost in ghost_list:
            if ghost: # is frightened
                # respawn the ghost
                # add to the score
                self.pacman.loose_life() # putting this here to test it
            else:
                pass

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        # pacman versus the ghosts
        hit_ghosts = arcade.check_for_collision_with_list(self.pacman, self.ghost_list)
        if hit_ghosts:
            self.handle_ghost_colision(hit_ghosts)

        if self.pacman.is_dying:
            self.pacman.update_death(delta_time)
            if self.pacman.is_dead:  # death animation has finished
                self.pacman.kill_pacman()
                if self.pacman.lives <= 0:
                    print("Game over")  # TODO: replace with a game over screen
            return  # freeze ghosts while dying

        self.ghost_list.update(delta_time=delta_time, pacman_pos=self.pacman.position)
        self.sprites.update(delta_time)
        self.physics_engine.update()
        for engine in self.ghost_engines:
            engine.update()

        hit_ghosts = arcade.check_for_collision_with_list(self.pacman, self.ghost_list)
        if hit_ghosts:
            self.handle_ghost_colision(hit_ghosts)

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        # block inputs while pacman is dying
        if self.pacman.is_dying:
            return
        # move pacman
        self.pacman.on_key_press(key, key_modifiers)

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        self.pacman.on_key_release(key, key_modifiers)

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
    """Main function"""

    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    # Create and set up the GameView
    game = GameView()

    game.setup()

    # Show GameView on screen
    window.show_view(game)

    # Start the arcade game loop
    arcade.run()


if __name__ == "__main__":
    main()
