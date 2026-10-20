import arcade
from pathlib import Path
from ghost import Ghost
import random

class Inky(Ghost):

    
    #TODO: create a dictionary of attributes based on color of the ghost
    def __init__(self):

        super().__init__()

        sprite_files = Path("../images/ghosts/inky")

        frames = [
            arcade.load_texture(str(frame))
            for frame in sprite_files.iterdir()
        ]

        self.frames = {
            "down": frames[:2],
            "left": frames[2:4],
            "right": frames[4:6],
            "up": frames[6:]
        }

        self.textures = self.frames["down"]
        self.texture = self.textures[0]
        self.center_x = random.randint(0, 1280)
        self.center_y = random.randint(0, 720)



    # def update_animation(self, direction):

    #     # make sure eyes are correct
    #     if direction[0] == 'x':
    #         if direction[1] > 0:
    #             self.textures = self.frames['right']
    #         else:
    #             self.textures = self.frames['left']

    #     else:
    #         if direction[1] > 0:
    #             self.textures = self.frames['up']
    #         else:
    #             self.textures = self.frames['down']

    #     self.cur_texture_index = (self.cur_texture_index + 1) % len(self.textures)
    #     self.texture = self.textures[self.cur_texture_index]

    # def update(self, delta_time):

    #     # movement logic
    #     start_x = self.center_x
    #     start_y = self.center_y

    #     self.dest_x = 500
    #     self.dest_y = 400

    #     x_diff = self.dest_x - start_x
    #     y_diff = self.dest_y - start_y

    #     #can only move orthogonally
    #     if x_diff:
    #         speed = min(self.speed, x_diff)
    #         self.center_x += speed
    #         direction = ('x', x_diff)
    #     elif y_diff:
    #         speed = min(self.speed, y_diff)
    #         self.center_y += speed
    #         direction = ('y', y_diff)
        
    #     #update the animation
    #     if self.animation_timer >= self.FRAME_DURATION:
    #         self.update_animation(delta_time=delta_time, direction=direction)
    #         self.animation_timer = 0


    #     self.elapsed_time += delta_time
    #     self.animation_timer += delta_time

        

        


"""
JUST TO GET THINGS TO DISPLAY
"""

# Constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Platformer"

class GameView(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

        # Variable to hold our texture for our player
        # self.player_texture = arcade.load_texture(
        #     ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        # )

        # Separate variable that holds the player sprite
        self.player_sprite = Ghost()
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128

        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        pass

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Draw our sprites
        arcade.draw_sprite(self.player_sprite)

    def on_update(self, delta_time):
        self.player_sprite.update(delta_time=delta_time)

def main():
    """Main function"""
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()