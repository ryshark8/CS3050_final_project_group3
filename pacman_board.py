#
# Script for first draft of gameboard
#

import arcade

# Board Configuration
TILE_SIZE = 20
COLS = 28
ROWS = 31
LABEL_POSITION = 32
HIGH_SCORE_POSITION = 12
SCORE_POSITION = 50
LABEL_SIZE = 14
SCORE_SIZE = 12

# RGB Colors
BACKGROUND = (5, 5, 12)
WALL_COLOR = (40, 50, 255)
WALL_FILL = (10, 10, 35)
PELLET_COLOR = (255, 220, 100)

# Window Configuration
MARGIN = 20
HEADER_HEIGHT = 55 # For score section

# Literal maze configuration
# '#' = wall, '.' = pellet, ' ' = empty

RAW_MAZE = [
    "############################",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#.####.#####.##.#####.####.#",
    "#..........................#",
    "#.####.##.########.##.####.#",
    "#......##....##....##......#",
    "######.##### ## #####.######",
    "     #.##### ## #####.#      ",
    "     #.##          ##.#      ",
    "######.## ###  ### ##.######",
    "      .   #      #   .      ",
    "######.## #      # ##.######",
    "     #.## ######## ##.#      ",
    "     #.##          ##.#      ",
    "######.## ######## ##.######",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#....#................#....#",
    "####.#.##.########.##.#.####",
    "#......##....##....##......#",
    "#.##########.##.##########.#",
    "#..........................#",
    "#.####.#####.##.#####.####.#",
    "#...##................##...#",
    "###.##.##.########.##.##.###",
    "#......##....##....##......#",
    "#.############ ############.#",
    "#..........................#",
    "############################",
]

# Verify dimensions
MAZE = [row.ljust(COLS)[:COLS] for row in RAW_MAZE]
ROWS = len(MAZE)

# Set window dimensions
BOARD_WIDTH = COLS * TILE_SIZE
BOARD_HEIGHT = ROWS * TILE_SIZE

SCREEN_WIDTH = BOARD_WIDTH + 2 * MARGIN
SCREEN_HEIGHT = BOARD_HEIGHT + HEADER_HEIGHT + 2 * MARGIN

HIGH_SCORE = "140"
CURRENT_SCORE = "100"

# Create window

class PacmanBoard(arcade.Window):
    def __init__(self):
        super().__init__(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            "Pac-Man Board 1"
        )

        arcade.set_background_color(BACKGROUND)

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

    # Draw maze
    def draw_maze(self):
        for row in range(ROWS):
            for col in range(COLS):
                cell = MAZE[row][col]
                x,y = self.cell_center(row, col)

                if cell == "#":
                    arcade.draw_rect_filled(
                        arcade.XYWH(
                            x, y,
                            TILE_SIZE - 2, TILE_SIZE - 2
                        ),
                        WALL_FILL
                    )

                    arcade.draw_rect_outline(
                        arcade.XYWH(
                            x, y,
                            TILE_SIZE - 2, TILE_SIZE - 2
                        ),
                        WALL_COLOR,
                        border_width = 2
                    )

                elif cell == ".":
                    arcade.draw_circle_filled(
                        x, y,
                        2.5,
                        PELLET_COLOR
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

