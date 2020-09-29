"""This bot decides randomly what action to take and in case of announcing what value to choose."""

import random

import lib.tools as tools
from lib.high_level_api import MaexchenHighLevelBotAPI
from time import sleep


def random_answer(previous_turn):
    rand = random.randint(0, 1)
    if rand and previous_turn is not None:
        bot.accuse()
    else:
        all_values = tools.valid_game_values_lowest_to_highest()
        if previous_turn is None:
            values_to_choose_from = all_values
        else:
            value = previous_turn[1]
            index = tools.value_to_rank(value)
            values_to_choose_from = all_values[index + 1:]

        bot.roll()
        announce_value = random.choice(values_to_choose_from)
        bot.announce(announce_value)


bot = MaexchenHighLevelBotAPI("true_random_bot")
bot.start()
bot.register_callback(random_answer)

while True:
    try:
        sleep(4)
    except KeyboardInterrupt:
        bot.close()
        exit(0)