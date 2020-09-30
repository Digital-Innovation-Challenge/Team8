from duckling.lib.high_level_api import MaexchenHighLevelBotAPI
from duckling.lib.tools import valid_game_values_lowest_to_highest
from time import sleep


class StrategyBot:
    """
    This bot is a basic bot that makes decisions based its given strategy.
    """

    def __init__(self, name, strategy):
        self.bot = MaexchenHighLevelBotAPI(name)
        self.strategy = strategy
        self.bot.register_callback(self.callback_receiver)

    def callback_receiver(self, prev_turn):
        prev_turns = self.bot.get_announced()
        if self.strategy.should_accuse(prev_turns):
            self.bot.accuse()
        else:
            roll = self.bot.roll()
            announcement = self.strategy.announce(prev_turns, roll)
            self.bot.announce(announcement)

    def exclude_trivialities(self, prev_turn, first_turn=None):
        if prev_turn is None:
            if first_turn is None:
                roll = self.bot.roll()
                self.bot.announce(roll)
            else:
                self.bot.roll()
                self.bot.announce(first_turn)
            return True
        elif prev_turn[1] == valid_game_values_lowest_to_highest()[-1]:
            self.bot.accuse()
            return True
        return False

    def run(self):
        self.bot.start()
        while True:
            try:
                sleep(42)
            except KeyboardInterrupt:
                self.bot.close()
                exit(0)
