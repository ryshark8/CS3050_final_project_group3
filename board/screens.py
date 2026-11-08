"""
Start and end screens for the game
"""

import arcade


class StartView(arcade.View):
    """
    Start screen first visible to user
    """

    def __init__(self, start_game):
        super().__init__()
        self.elapsed_time = 0
        self.start_game = start_game
        self.background_color = (5, 5, 12)
        self.background = arcade.load_texture("images/start_screen.png")
        self.text = arcade.Text(
            "Press ENTER to Start",
            self.window.width / 2,
            250,
            arcade.color.YELLOW,
            font_size=15,
            anchor_x="center",
        )

        print(self.window.height / 2)

    def on_draw(self):
        self.clear()
        image = arcade.LBWH(self.window.width / 10, self.window.height / 2, 4 * self.window.width / 5, 200)

        arcade.draw_texture_rect(self.background, image)

        self.text.draw()

    def on_key_press(self, symbol, modifers):

        if symbol == arcade.key.ENTER:
            self.start_game()
            print("enter hit")

    
    def on_update(self, delta_time):
        
        if self.elapsed_time > 1:

            if self.text.color == arcade.color.YELLOW:
                self.text.color = arcade.color.DARK_YELLOW

            else:
                self.text.color = arcade.color.YELLOW

            self.elapsed_time = 0

        self.elapsed_time += delta_time


class GameOverView(arcade.View):
    """
    Screen visible when player loses
    """

    def __init__(self, start_game):
        super().__init__()
        self.elapsed_time = 0
        self.start_game = start_game
        self.background_color = (5, 5, 12)
        self.background = arcade.load_texture("images/start_screen.png")
        self.game_over = arcade.Text(
            "GAME OVER",
            self.window.width / 2,
            self.window.height / 2,
            arcade.color.YELLOW,
            font_size=22,
            anchor_x="center",
        )
        self.instructions = arcade.Text(
            "press ENTER to play again",
            self.window.width / 2,
            self.window.height / 2 - 50,
            arcade.color.YELLOW,
            font_size=15,
            anchor_x="center",
        )

    def on_draw(self):
        self.clear()

        self.game_over.draw()
        self.instructions.draw()

    def on_update(self, delta_time):
        if self.elapsed_time > 1:
        
            if self.instructions.color == arcade.color.YELLOW:
                self.instructions.color = arcade.color.DARK_YELLOW

            else:
                self.instructions.color = arcade.color.YELLOW

            self.elapsed_time = 0
    
        self.elapsed_time += delta_time
        

    def on_key_press(self, symbol, modifers):

        if symbol == arcade.key.ENTER:
            self.start_game()
            print("enter hit")
