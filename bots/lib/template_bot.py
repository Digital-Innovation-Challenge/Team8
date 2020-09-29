from lib.high_level_api import MaexchenHighLevelBotAPI
from lib.tools import valid_game_values_lowest_to_highest
from time import sleep


class TemplateBot:
    """
    This bot is a template and always times out.
    It is supposed to be extended overridden by other bots which override the callback_receiver.
    """

    def __init__(self, name):
        self.bot = MaexchenHighLevelBotAPI(name)
        self.bot.register_callback(self.callback_receiver)

    def callback_receiver(self, prev_turn):
        """Override this method to add functionality to your bot."""
        pass

    def exclude_trivialities(self, prev_turn):
        if prev_turn is None:
            roll = self.bot.roll()
            self.bot.announce(roll)
        elif prev_turn[1] == valid_game_values_lowest_to_highest()[-1]:
            self.bot.accuse()

    def run(self):
        self.bot.start()
        while True:
            try:
                sleep(42)
            except KeyboardInterrupt:
                self.bot.close()
                exit(0)


if __name__ == "__main__":
    TemplateBot("template-bot").run()
