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
from board.levels import level1_board, level2_board, level
from board.dots_and_fruits.fruits import Fruit, fruit_for_level, LEVEL_FRUIT

from board.ghosts.blinky import Blinky
from board.ghosts.pinky import Pinky
from board.ghosts.inky import Inky
from board.ghosts.clyde import Clyde

from pacman import Pacman

from board.screens import StartView, GameOverView

from config import (
    BOARD_WIDTH,
    BOARD_HEIGHT,
    TILE_SIZE,
    MARGIN,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_TITLE,
    DEBUG,
)


class GameState:
    """Initialize game state variables"""

    def __init__(self):
        self.levels = [Level(level1_board.maze), Level(level2_board.maze)]
        self.current_level = 0
        self.current_score = 0
        self.dots_eaten = 0
        self.mega_dots_eaten = 0

    # Initialize for each level
    def initialize_level(self):
        self.dots_eaten = 0
        self.mega_dots_eaten = 0
        self.current_score = 0

    # Update current score
    def add_score(self, points):
        self.current_score += points

    def collect_dot(self):
        self.dots_eaten += 1

    def collect_mega_dot(self):
        self.mega_dots_eaten += 1

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

        # was this:
        # self.pacman_walls = arcade.SpriteList()
        # basically what I learned is that this is bad
        # it copies all of the walls into a plain list
        # then when we do a collision check we have to loop over
        # all of the walls which is about 1500, eeek
        # my hope is that this fixes it
        # commenting because we might need to do the same thing for ghosts

        self.pacman_walls = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=32
        )

        self.pacman_walls.extend(wall_list)
        self.pacman_walls.extend(ghost_wall_list)

        pacman.walls = self.pacman_walls

        self.pacman_engine = arcade.PhysicsEngineSimple(pacman, self.pacman_walls)

    def update_pacman(self):
        self.pacman_engine.update()


class GameObjects:

    def __init__(self):
        self.fruit_list = None
        self.dot_list = None
        self.mega_dot_list = None
        self.num_dots = None

    def dot_count(self, board):
        self.dot_list = board.dot_list
        self.mega_dot_list = board.mega_dot_list
        self.num_dots = len(self.dot_list) + len(self.mega_dot_list)

    def spawn_fruit(self, current_level, position):

        if len(self.fruit_list) == 0:  # only one at a time
            kind = fruit_for_level(current_level)
            self.fruit_list.append(Fruit(kind, *position))

            if DEBUG:
                print(f"Spawned: {kind}")


class GameView(arcade.View):
    """
    Main application class.
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
        self.objects.mega_dot_list = arcade.SpriteList()
        self.objects.fruit_list = arcade.SpriteList()

        self.state.dots_eaten = 0
        self.state.mega_dots_eaten = 0
        self.next_fruit_index = 0
        self.objects.dot_count(self.board)

        self.create_pacman()
        self.create_ghosts(
            jail_center=level.find_jail_center(),
            board_rows=level.rows,
            board_cols=level.cols,
        )

    def get_spawn_point(self):
        """Finds the open corridor just below the jail center"""
        jail_x, jail_y = self.board.level.find_jail_center()
        return jail_x, jail_y - 7 * TILE_SIZE

    def create_pacman(self):
        # calculated spawn coords to replace the hardcoded ones before
        # turned this into a helper so I can use in fruits too
        spawn_x, spawn_y = self.get_spawn_point()

        self.pacman = Pacman(spawn_x, spawn_y)
        self.sprites.append(self.pacman)

        # call the physics engine for collisions
        self.physics.pacman_physics(
            self.pacman, self.board.wall_list, self.board.ghost_wall_list
        )

    def create_ghosts(self, jail_center, board_cols, board_rows):

        self.ghost_list = arcade.SpriteList()

        self.ghost_list.extend(
            [
                Blinky(jail_center),
                Inky(jail_center, board_cols=board_cols, board_rows=board_rows),
                Pinky(jail_center, board_cols=board_cols, board_rows=board_rows),
                Clyde(jail_center, board_cols=board_cols, board_rows=board_rows),
            ]
        )

        barrier_list = arcade.AStarBarrierList(
            moving_sprite=self.ghost_list[0],
            blocking_sprites=self.board.wall_list,
            grid_size=TILE_SIZE,
            left=0,
            right=board_cols * TILE_SIZE,
            bottom=0,
            top=board_rows * TILE_SIZE,
        )

        for ghost in self.ghost_list:
            ghost.barrier_list = barrier_list

    def reset(self):
        """Reset the game to the initial state."""
        self.setup()
        # Do needed changes to restart the game here if you want to support that

    def spawn_fruit(self):
        self.objects.spawn_fruit(self.state.current_level, self.get_spawn_point())

    # handle what happens when ghost and pacman collide
    def handle_ghost_collision(self, ghost_list):
        for ghost in ghost_list:
            # TODO: this is where the ghost eaten logic should go!
            if ghost:  # is frightened
                # respawn the ghost
                # add to the score
                self.pacman.loose_life()  # putting this here to test it
            else:
                pass

    # handle dot collision
    def handle_dot_collision(self, hit_list):
        for dot in hit_list:
            self.state.collect_dot()
            self.add_score(10)
            dot.remove_from_sprite_lists()

            if DEBUG:
                print(
                    f"Score: {self.state.current_score}, "
                    f"Dots eaten: {self.state.dots_eaten}"
                )

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

    # handle mega dot collision
    def handle_mega_dot_collision(self, hit_list):
        for mega_dot in hit_list:
            self.state.collect_mega_dot()
            self.add_score(40)
            mega_dot.remove_from_sprite_lists()

            if DEBUG:
                print(
                    f"Score: {self.state.current_score}, "
                    f"Mega Dots eaten: {self.state.mega_dots_eaten}"
                )

    def add_score(self, points):
        self.state.add_score(points)

        self.board.current_score_number.text = str(self.state.current_score)

    def update_game(self, delta_time):
        self.ghost_list.update(delta_time=delta_time, pacman_pos=self.pacman.position)

        self.sprites.update(delta_time)
        self.physics.update_pacman()

        # Check collision after movement
        hit_ghosts = arcade.check_for_collision_with_list(self.pacman, self.ghost_list)

        if hit_ghosts:
            self.handle_ghost_collision(hit_ghosts)

        hit_dots = arcade.check_for_collision_with_list(
            self.pacman, self.objects.dot_list
        )

        if hit_dots:
            self.handle_dot_collision(hit_dots)

        hit_mega_dots = arcade.check_for_collision_with_list(
            self.pacman, self.objects.mega_dot_list
        )

        if hit_mega_dots:
            self.handle_mega_dot_collision(hit_mega_dots)

        self.objects.fruit_list.update(delta_time=delta_time)

        self.objects.fruit_list.update(delta_time=delta_time)

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
                        self.display_game_over(self.window)
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

    def start_game(self, window):
        """start a new game"""
        game = GameView()
        game.setup()
        window.show_view(game)

    def display_start_screen(self, window):
        """display the start screen"""
        start_view = StartView(lambda: self.start_game(window))
        window.show_view(start_view)

    def display_game_over(self, window):
        """display the game over screen"""
        game_over = GameOverView(lambda: self.start_game(window))
        window.show_view(game_over)


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
