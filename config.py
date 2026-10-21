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
HEADER_HEIGHT = 55 # For score section

LINE_COLOR = (40, 50, 255)
FILL_COLOR = (10, 10, 100)

# Debug constants
DEBUG = True
