"""
A file for keeping global constants
"""

# window constants
WINDOW_WIDTH = 550
WINDOW_HEIGHT = 700
WINDOW_TITLE = "Pac-Man"

# board constants
BOARD_WIDTH = 510
BOARD_HEIGHT = 600
BOARD_SIZE = BOARD_WIDTH * BOARD_HEIGHT

#where the board is w/ respect to the window
difference_w = WINDOW_WIDTH - BOARD_WIDTH
difference_h = WINDOW_HEIGHT - BOARD_HEIGHT
BOARD_BOUNDARIES = ([difference_w / 2, WINDOW_WIDTH - (difference_w / 2)], [difference_h / 2, WINDOW_HEIGHT - (difference_h / 2)]) 


MARGIN = 20
HEADER_HEIGHT = 55

TILE_SIZE = 15
LABEL_SIZE = 14
SCORE_SIZE = 12
LABEL_POSITION = 32
SCORE_POSITION = 50
HIGH_SCORE_POSITION = 12

LINE_COLOR = (40, 50, 255)
FILL_COLOR = (10, 10, 100)

# Debug constants
DEBUG = True
