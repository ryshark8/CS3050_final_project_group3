
from config import *

# Board Configuration
tile_size = 15
label_size = 14
score_size = 12
label_position = 32
high_score_position = 12
score_position = 50

# Window Configuration
margin = MARGIN
header_height = HEADER_HEIGHT

raw_maze = [
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
    "#######  ##  ###--###  ##  #######",
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

# Get dimensions
rows = len(raw_maze)
cols = len(raw_maze[0])

# Verify maze dimensions
maze = [row.ljust(cols)[:cols] for row in raw_maze]

# Set board dimensions
board_width = cols * tile_size
board_height = rows * tile_size

screen_width = board_width + 2 * margin
screen_height = board_height + header_height + 2 * margin
