import random

import lib.tools as tools
from lib.template_bot import TemplateBot

accuse_percentage = 0.1


class RandomBot(TemplateBot):
    """
    This bot decides randomly what action to take and in case of announcing what value to choose.
    """

    # overridden
    def callback_receiver(self, prev_turn):
        TemplateBot.exclude_trivialities(prev_turn)

        accuse = random.random() < accuse_percentage
        if accuse:
            self.bot.accuse()
        else:
            all_values = tools.valid_game_values_lowest_to_highest()
            if prev_turn is None:
                values_to_choose_from = all_values
            else:
                value = prev_turn[1]
                index = tools.value_to_rank(value)
                values_to_choose_from = all_values[index + 1:]

            self.bot.roll()
            announce_value = random.choice(values_to_choose_from)
            self.bot.announce(announce_value)


if __name__ == "__main__":
    bot = RandomBot("true_random_bot")
    bot.run()
