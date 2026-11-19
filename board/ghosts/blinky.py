"""Red ghost"""

from pathlib import Path
from board.ghosts.ghost import Ghost


class Blinky(Ghost):
    """Child class for the red ghost"""

    def __init__(self, jail_center):

        super().__init__(jail_center, sprite_files=Path("images/ghosts/blinky"))
        self.center_x = self.jail_center[0]
        self.center_y = self.jail_center[1] + self.width + 20
        self.mode = self.Mode.CHASE
        self.destination = None
