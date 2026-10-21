
import arcade

class Level:
    def __init__(self, tile_size, label_size, score_size, label_position, score_position,
                 high_score_position, margin, header_height, rows, cols, maze,
                 screen_width, screen_height, board_width, board_height):

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

