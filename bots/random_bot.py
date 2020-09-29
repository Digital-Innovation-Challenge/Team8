"""This bot decides randomly what action to take and in case of announcing what value to choose."""

import random

import lib.tools as tools
from lib.high_level_api import MaexchenHighLevelBotAPI
from time import sleep

accuse_percentage = 0.1


def random_answer(previous_turn):
    accuse = random.random() < accuse_percentage
    all_values = tools.valid_game_values_lowest_to_highest()
    if previous_turn is not None and (accuse or previous_turn[1] == all_values[-1]):
        bot.accuse()
    else:
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
