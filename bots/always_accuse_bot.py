"""This bot always accuses except on the first turn where it announces the truth."""

from lib.high_level_api import MaexchenHighLevelBotAPI
from time import sleep


def always_accuse(prev_turn):
    if prev_turn is None:
        roll = bot.roll()
        bot.announce(roll)
    else:
        bot.accuse()


bot = MaexchenHighLevelBotAPI("always_accuse")
bot.start()
bot.register_callback(always_accuse)

while True:
    try:
        sleep(42)
    except KeyboardInterrupt:
        bot.close()
        exit(0)
