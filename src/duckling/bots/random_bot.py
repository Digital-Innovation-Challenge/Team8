import random

import duckling.lib.tools as tools
from duckling.bots.template_bot import TemplateBot
import duckling.bots.strategies as strategies

accuse_percentage = 0.1


class RandomBot(TemplateBot):
    """
    This bot decides randomly what action to take and in case of announcing what value to choose.
    """

    def __init__(self, *args, **kwargs):
        super(RandomBot, self).__init__(*args, **kwargs)
        self._random_strategy = strategies.RandomStrategy()
        
    # overridden
    def callback_receiver(self, prev_turn):
        self._random_strategy.trivialities(prev_turn)
        
        if self._random_strategy.should_accuse():
            self.bot.accuse()
        else:
            self.bot.roll
            self.bot.announce(self._random_strategy.announce(prev_turn))
        

        # else:
        #     all_values = tools.valid_game_values_lowest_to_highest()
        #     if prev_turn is None:
        #         values_to_choose_from = all_values
        #     else:
        #         value = prev_turn[1]
        #         index = tools.value_to_rank(value)
        #         values_to_choose_from = all_values[index + 1:]
        #     self.bot.roll()
        #     announce_value = random.choice(values_to_choose_from)
        #     self.bot.announce(announce_value)

if __name__ == "__main__":
    bot = RandomBot("true_random_bot")
    bot.run()
