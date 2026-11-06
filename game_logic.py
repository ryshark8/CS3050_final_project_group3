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
from board import pacman_board
from board.levels.level import Level
from board.levels import level1_board, level2_board
from board.dots_and_fruits.fruits import Fruit, fruit_for_level, LEVEL_FRUIT

from board.ghosts.blinky import Blinky
from board.ghosts.pinky import Pinky
from board.ghosts.inky import Inky
from board.ghosts.clyde import Clyde

from pacman import Pacman

from config import (BOARD_WIDTH, BOARD_HEIGHT, TILE_SIZE,
                    MARGIN, WINDOW_WIDTH, WINDOW_HEIGHT,
                    WINDOW_TITLE, DEBUG)


class GameState:
    """ Initialize game state variables """

    def __init__(self):
        self.levels = [
            Level(level1_board.maze),
            Level(level2_board.maze)
        ]
        self.current_level = 0
        self.current_score = 0
        self.dots_eaten = 0

    # Initialize for each level
    def initialize_level(self):
        self.dots_eaten = 0
        self.current_score = 0

    # Update current score
    def add_score(self, points):
        self.current_score += points

    def collect_dot(self):
        self.dots_eaten += 1

    def advance_level(self):
        if self.current_level < len(self.levels) - 1:
            self.current_level += 1
        else:
            if DEBUG:
                print("Game completed")  # TODO: Game completion screen


class GamePhysics:
    """Initialize game physics"""

    def __init__(self):
        self.pacman_walls = None
        self.pacman_engine = None
        self.ghost_engines = []
        self.barrier_list = None

    def pacman_physics(self, pacman, wall_list, ghost_wall_list):

        self.pacman_walls = arcade.SpriteList()

        self.pacman_walls.extend(wall_list)
        self.pacman_walls.extend(ghost_wall_list)

        pacman.walls = self.pacman_walls

        self.pacman_engine = arcade.PhysicsEngineSimple(
            pacman, self.pacman_walls
        )

    def setup_ghost_engines(self, ghost_list, wall_list):
        # one engine for each of the ghosts
        self.ghost_engines = [
            arcade.PhysicsEngineSimple(ghost, wall_list)
            for ghost in ghost_list
        ]

    def update_pacman(self):
        self.pacman_engine.update()

    def update_ghosts(self):
        for engine in self.ghost_engines:
            engine.update()


class GameObjects:

    def __init__(self):
        self.fruit_list = None
        self.dot_list = None
        self.num_dots = None

    def dot_count(self, board):
        self.dot_list = board.dot_list
        self.num_dots = len(self.dot_list)

    def spawn_fruit(self, current_level):
        # self.fruit_list = arcade.SpriteList()

        if len(self.fruit_list) == 0:  # only one at a time
            kind = fruit_for_level(current_level)
            self.fruit_list.append(Fruit(kind, 265, 247))

            if DEBUG:
                print(f"Spawned: {kind}")

class GameView(arcade.View):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self):
        super().__init__()

        # Initial configurations
        self.background_color = (5, 5, 12)

        self.state = GameState()
        self.physics = GamePhysics()
        self.objects = GameObjects()

        self.board = None
        self.pacman = None
        self.ghost_list = None
        self.sprites = None

        self.next_fruit_index = 0

    def setup(self):

        level = self.state.levels[self.state.current_level]

        self.board = pacman_board.PacmanBoard(level)

        self.state.initialize_level()

        # ---------- sprites --------------
        # pacman
        self.sprites = arcade.SpriteList()
        # Fruits
        self.objects.dot_list = arcade.SpriteList()
        self.objects.fruit_list = arcade.SpriteList()

        self.state.dots_eaten = 0
        self.next_fruit_index = 0
        self.objects.dot_count(self.board)

        self.create_pacman()
        self.create_ghosts()

    def create_pacman(self):
        # coords for where to spawn pacman, right below the ghost prison or whatever
        spawn_x = 250
        spawn_y = 258

        self.pacman = Pacman(spawn_x, spawn_y)
        self.sprites.append(self.pacman)

        # call the physics engine for collisions
        self.physics.pacman_physics(
            self.pacman, self.board.wall_list, self.board.ghost_wall_list
        )

    def create_ghosts(self):

        barrier_list = arcade.AStarBarrierList(
            moving_sprite = self.pacman,
            blocking_sprites = self.board.wall_list,
            grid_size = TILE_SIZE,
            left = MARGIN,
            right = MARGIN + BOARD_WIDTH,
            bottom = MARGIN,
            top = MARGIN + BOARD_HEIGHT,
        )

        self.ghost_list = arcade.SpriteList()

        self.ghost_list.extend([
                Inky(barrier_list),
                #Blinky(barrier_list),
                Pinky(barrier_list),
                Clyde(barrier_list),
            ])

    def reset(self):
        """Reset the game to the initial state."""
        self.setup()
        # Do needed changes to restart the game here if you want to support that

    def spawn_fruit(self):
        self.objects.spawn_fruit(self.state.current_level)

    # handle what happens when ghost and pacman collide
    def handle_ghost_collision(self, ghost_list):
        for ghost in ghost_list:
            if ghost: # is frightened
                # respawn the ghost
                # add to the score
                self.pacman.loose_life() # putting this here to test it
            else:
                pass

    # handle dot collision
    def handle_dot_collision(self, hit_list):
        for dot in hit_list:
            self.state.collect_dot()
            self.add_score(10)
            dot.remove_from_sprite_lists()

            if DEBUG:
                print(f"Score: {self.state.current_score}, "
                      f"Dots eaten: {self.state.dots_eaten}")

            # (70, 160) here is the threshold for spawning fruits
            # so when you eat 70 one spawns and when you eat 157 one spawns
            # In the real game it is 170, but we do not have enough dots on the board
            # there are 157 dots on the board
            if self.state.dots_eaten in (70, 157):
                self.spawn_fruit()

            if self.state.dots_eaten == self.objects.num_dots:
                self.state.advance_level()

                if self.state.current_level < len(self.state.levels):
                    self.reset()

                return

    def add_score(self, points):
        self.state.add_score(points)

        self.board.current_score_number.text = str(self.state.current_score)

    def update_game(self, delta_time):
        self.ghost_list.update(
            delta_time = delta_time,
            pacman_pos = self.pacman.position
        )

        self.sprites.update(delta_time)
        self.physics.update_pacman()
        self.physics.update_ghosts()

        # Check collision after movement
        hit_ghosts = arcade.check_for_collision_with_list(
            self.pacman, self.ghost_list
        )

        if hit_ghosts:
            self.handle_ghost_collision(hit_ghosts)

        hit_dots = arcade.check_for_collision_with_list(
            self.pacman, self.objects.dot_list
        )

        if hit_dots:
            self.handle_dot_collision(hit_dots)

        self.objects.fruit_list.update(delta_time=delta_time)

        self.objects.fruit_list.update(delta_time = delta_time)

        hit_fruits = arcade.check_for_collision_with_list(
            self.pacman, self.objects.fruit_list
        )

        for fruit in hit_fruits:
            self.add_score(fruit.points)
            fruit.remove_from_sprite_lists()

            if DEBUG:
                print(
                    f"Pacman ate a {fruit.kind} + {fruit.points} points\n"
                    f"Score: {self.state.current_score}, Dots eaten: {self.state.dots_eaten}"
                )


    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.


        # Call draw() on all your sprite lists below
        self.clear()

        # Call draw() on all your sprite lists below
        self.board.draw()
        self.ghost_list.draw()
        self.sprites.draw()
        self.objects.fruit_list.draw()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """

        if self.pacman.is_dying:
            self.pacman.update_death(delta_time)

            if self.pacman.is_dead:  # death animation has finished
                self.pacman.kill_pacman()

                if self.pacman.lives <= 0:
                    if DEBUG:
                        print("Game over")  # TODO: replace with a game over screen
            return  # freeze ghosts while dying

        self.update_game(delta_time)

    def on_key_press(self, symbol, modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        # block inputs while pacman is dying
        if self.pacman.is_dying:
            return
        # move pacman
        self.pacman.on_key_press(symbol, modifiers)


def main():
    """Main function"""

    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(
        WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE
    )

    # Create and set up the GameView
    game = GameView()
    game.setup()

    # Show GameView on screen
    window.show_view(game)

    # Start the arcade game loop
    arcade.run()


if __name__ == "__main__":
    main()
