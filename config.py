"""
A file for keeping global constants
"""

# window constants
# ------ ross edit -----
# was 517 switched to 486 to center it
WINDOW_WIDTH = 486
WINDOW_HEIGHT = 653
WINDOW_TITLE = "Pac-Man"

# board constants
BOARD_WIDTH = 510
BOARD_HEIGHT = 600
BOARD_SIZE = BOARD_WIDTH * BOARD_HEIGHT

# where the board is w/ respect to the window
DIFFERENCE_W = WINDOW_WIDTH - BOARD_WIDTH
difference_h = WINDOW_HEIGHT - BOARD_HEIGHT
BOARD_BOUNDARIES = (
    [DIFFERENCE_W // 2, WINDOW_WIDTH - (DIFFERENCE_W // 2)],
    [difference_h // 2, WINDOW_HEIGHT - (difference_h // 2)],
)

# jail coordinates
JAIL_CENTER = (253, 315)

MARGIN = 20
HEADER_HEIGHT = 55

TILE_SIZE = 9
LABEL_SIZE = 14
SCORE_SIZE = 12
LABEL_POSITION = 32
SCORE_POSITION = 50
HIGH_SCORE_POSITION = 12

LINE_COLOR = (40, 50, 255)
FILL_COLOR = (10, 10, 100)

# Debug constant
DEBUG = True
