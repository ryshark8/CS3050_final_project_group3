#
# Script for first draft of gameboard
#

import arcade
from arcade import BasicSprite

# Board Configuration
TILE_SIZE = 15
COLS = 28
LABEL_POSITION = 32
HIGH_SCORE_POSITION = 12
SCORE_POSITION = 50
LABEL_SIZE = 14
SCORE_SIZE = 12

# RGB Colors
BACKGROUND = (5, 5, 12)
WALL_COLOR = (40, 50, 255)
WALL_FILL = (10, 10, 25)
PELLET_COLOR = (255, 220, 100)

# Window Configuration
MARGIN = 20
HEADER_HEIGHT = 55 # For score section

# Literal maze configuration
# '#' = wall, '.' = pellet, ' ' = empty

RAW_MAZE = [
    "##################################",
    "#               ##               #",
    "#               ##               #",
    "#  ####  #####  ##  #####  ####  #",
    "#  ####  #####  ##  #####  ####  #",
    "#  ####  #####  ##  #####  ####  #",
    "#                                #",
    "#                                #",
    "#  ####  ##  ########  ##  ####  #",
    "#  ####  ##  ########  ##  ####  #",
    "#        ##     ##     ##        #",
    "#        ##     ##     ##        #",
    "#######  #####  ##  #####  #######",
    "      #  #####  ##  #####  #      ",
    "      #  ##            ##  #      ",
    "      #  ##            ##  #      ",
    "#######  ##  ###  ###  ##  #######",
    "             #      #             ",
    "             #      #             ",
    "#######  ##  #      #  ##  #######",
    "      #  ##  ########  ##  #      ",
    "      #  ##            ##  #      ",
    "      #  ##            ##  #      ",
    "#######  ##  ########  ##  #######",
    "#######  ##  ########  ##  #######",
    "#               ##               #",
    "#               ##               #",
    "#  ####  #####  ##  #####  ####  #",
    "#  ####  #####  ##  #####  ####  #",
    "#    ##                    ##    #",
    "#    ##                    ##    #",
    "###  ##  ##  ########  ##  ##  ###",
    "###  ##  ##  ########  ##  ##  ###",
    "#        ##     ##     ##        #",
    "#        ##     ##     ##        #",
    "#  ###########  ##  ###########  #",
    "#  ###########  ##  ###########  #",
    "#                                #",
    "#                                #",
    "##################################"
]

# Verify dimensions
for line in RAW_MAZE:
   COLS = len(line)
MAZE = [row.ljust(COLS)[:COLS] for row in RAW_MAZE]
ROWS = len(MAZE)

# Set window dimensions
BOARD_WIDTH = COLS * TILE_SIZE
BOARD_HEIGHT = ROWS * TILE_SIZE

SCREEN_WIDTH = BOARD_WIDTH + 2 * MARGIN
SCREEN_HEIGHT = BOARD_HEIGHT + HEADER_HEIGHT + 2 * MARGIN

HIGH_SCORE = "140"
CURRENT_SCORE = "100"

class Wall(arcade.SpriteSolidColor):

    def __init__(self,x,y):

        super().__init__(
            width=TILE_SIZE+2, height=TILE_SIZE+2,
            color=WALL_COLOR,
            center_x=x, center_y=y
        )

# Create window

class PacmanBoard(arcade.Window):
    def __init__(self):
        super().__init__(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            "Pac-Man Board 1"
        )

        arcade.set_background_color(BACKGROUND)

        self.wall_list = arcade.SpriteList()

        self.create_walls()

        self.high_score_label = arcade.Text(
            "HIGH SCORE",
            SCREEN_WIDTH / 2,
            MARGIN + BOARD_HEIGHT + LABEL_POSITION,
            arcade.color.WHITE,
            font_size = LABEL_SIZE,
            anchor_x = "center"
        )

        # Create the high-score number.
        self.high_score_number = arcade.Text(
            "140",
            SCREEN_WIDTH / 2,
            MARGIN + BOARD_HEIGHT + HIGH_SCORE_POSITION,
            arcade.color.WHITE,
            font_size = SCORE_SIZE,
            anchor_x = "center"
        )

        self.current_score_label = arcade.Text(
            "CURRENT SCORE",
            MARGIN + SCORE_POSITION,
            MARGIN + BOARD_HEIGHT + LABEL_POSITION,
            arcade.color.WHITE,
            font_size = LABEL_SIZE,
            anchor_x = "center"
        )

        # Create the current-score number on the left.
        self.current_score = arcade.Text(
            "0",
            MARGIN + SCORE_POSITION,
            MARGIN + BOARD_HEIGHT + HIGH_SCORE_POSITION,
            arcade.color.WHITE,
            font_size = SCORE_SIZE,
            anchor_x = "center"
        )

    def on_draw(self):
        self.clear()
        self.draw_header()
        self.draw_maze()

    # Convert grid coordinates to screen coordinates
    def cell_center(self, row, col):
        # Find horizontal center of tile
        x = MARGIN + col * TILE_SIZE + TILE_SIZE / 2
        # Find vertical center of tile
        y = MARGIN + (ROWS - 1 - row) * TILE_SIZE + TILE_SIZE / 2
        return x, y

    # Create Walls
    def create_walls(self):
        for row in range(ROWS):
            for col in range(COLS):
                if MAZE[row][col] == "#":
                    x, y = self.cell_center(row, col)

                    wall = Wall(x,y)

                    self.wall_list.append(wall)

    # Draw maze
    def draw_maze(self):

        self.wall_list.draw()

        # Wall outline
        for wall in self.wall_list:
            arcade.draw_rect_filled(
                arcade.XYWH(
                    wall.center_x, wall.center_y,
                    TILE_SIZE, TILE_SIZE
                ),
                WALL_FILL
            )


    def draw_header(self):
        # Draw the existing text objects on the screen.
        self.high_score_label.draw()
        self.high_score_number.draw()
        self.current_score_label.draw()
        self.current_score.draw()


if __name__ == '__main__':
    game = PacmanBoard()
    arcade.run()

