"""
Start and end screens for the game
"""

import arcade
import csv
import os


class StartView(arcade.View):
    """
    Start screen first visible to user
    """

    def __init__(self, start_game):
        super().__init__()
        self.elapsed_time = 0
        self.start_game = start_game
        self.username = ''
        self.background_color = (5, 5, 12)
        self.background = arcade.load_texture("images/start_screen.png")

        self.start_text = arcade.Text(
            "Press ENTER to Start",
            self.window.width / 2,
            150,
            arcade.color.YELLOW,
            font_size=15,
            anchor_x="center",
        )

        # Username prompt
        self.username_text = arcade.Text(
            "ENTER PLAYER NAME:",
            self.window.width / 2,
            250,
            arcade.color.WHITE,
            font_size=18,
            anchor_x="center",
        )

        self.username_imput = arcade.Text(
            "",
            self.window.width / 2,
            200,
            arcade.color.WHITE,
            font_size=15,
            anchor_x="center",
        )

        print(self.window.height / 2)

    def on_draw(self):
        self.clear()

        image = arcade.LBWH(
            self.window.width / 10,
            self.window.height / 2,
            4 * self.window.width / 5,
            200,
        )

        arcade.draw_texture_rect(self.background, image)

        self.start_text.draw()
        self.username_text.draw()

        # Update Username as it's typed
        self.username_imput.text = self.username + "|"
        self.username_imput.draw()

    def on_text(self, text):
        if len(self.username) < 12:
            self.username += text

    def on_key_press(self, symbol, modifiers):

        # Start game on enter
        if symbol == arcade.key.ENTER:
            if self.username.strip():
                self.start_game()
            print("enter hit")

        # Backspace
        elif symbol == arcade.key.BACKSPACE:
            self.username = self.username[:-1]


    def on_update(self, delta_time):

        if self.elapsed_time > 1:

            if self.start_text.color == arcade.color.YELLOW:
                self.start_text.color = arcade.color.DARK_YELLOW

            else:
                self.start_text.color = arcade.color.YELLOW

            self.elapsed_time = 0

        self.elapsed_time += delta_time


class GameOverView(arcade.View):
    """
    Screen visible when player loses
    """

    def __init__(self, start_game, player_name, player_score):
        super().__init__()
        self.elapsed_time = 0
        self.start_game = start_game
        self.leaderboard = Leaderboard()
        self.scores = self.leaderboard.add_score(player_name, player_score)

        self.background_color = (5, 5, 12)
        self.background = arcade.load_texture("images/start_screen.png")
        start_y = self.window.height / 2
        line_offset = 50

        self.game_over = arcade.Text(
            "GAME OVER",
            self.window.width / 2,
            start_y,
            arcade.color.YELLOW,
            font_size=22,
            anchor_x="center",
        )
        self.score_title = arcade.Text(
            "HIGH SCORES",
            self.window.width / 2,
            start_y - line_offset,
            arcade.color.YELLOW,
            font_size=20,
            anchor_x="center",
        )
        self.score_text = []
        for index, entry in enumerate(self.scores):
            line = f"{entry['username']}    {entry['score']}"
            line_text = arcade.Text(
                line,
                self.window.width / 2,
                start_y - (index + 1) * line_offset,
                arcade.color.WHITE,
                font_size=15,
                anchor_x="center",
            )
            self.score_text.append(line_text)

        self.instructions = arcade.Text(
            "press ENTER to play again",
            self.window.width / 2,
            start_y - 11 * line_offset,
            arcade.color.YELLOW,
            font_size=15,
            anchor_x="center",
        )

    def on_draw(self):
        self.clear()

        self.game_over.draw()
        self.score_title.draw()
        for line in self.score_text:
            line.draw()
        self.instructions.draw()

    def on_update(self, delta_time):
        if self.elapsed_time > 1:

            if self.instructions.color == arcade.color.YELLOW:
                self.instructions.color = arcade.color.DARK_YELLOW

            else:
                self.instructions.color = arcade.color.YELLOW

            self.elapsed_time = 0

        self.elapsed_time += delta_time

    def on_key_press(self, symbol, modifiers):

        if symbol == arcade.key.ENTER:
            self.start_game()
            print("enter hit")


class Leaderboard:
    def __init__(self, filename = "pacman_leaderboard.csv"):
        self.filename = filename

        # Create new csv file if one doesn't exist yet
        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline = '') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["username", "score"])

    def get_scores(self):
        scores = []

        with open(self.filename, "r", newline = '') as csvfile:
            reader = csv.DictReader(csvfile)

            while len(scores) <= 10:
                for row in reader:
                        scores.append((row["username"], int(row["score"])))

        return scores

    def add_score(self, username, score):
        scores = self.get_scores()

        scores.append((username, score))

        scores.sort(key=lambda x: x[1], reverse = True)

        scores = scores[:10]

        with open(self.filename, "w", newline = '') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["username", "score"])
            writer.writerows(scores)

        return scores