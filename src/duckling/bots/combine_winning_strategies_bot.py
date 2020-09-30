from lib.template_bot import TemplateBot
from lib.tools import probability_of_value_above, higher_than, rank_to_value, value_to_rank
from random_bot import RandomBot
from conservative_strategy_bot import ConservativeStrategyBot
from aggressive_strategy_bot import AggressiveStrategyBot
import random

class CombineStrategyBot(TemplateBot):
    """
    This bot randomly chooses one winning strategy. 
    """
    def __init__(self, *args,**kwargs):
        super(CombineStrategyBot, self).__init__(*args, **kwargs)
        self._random_bot = RandomBot(*args, **kwargs)
        self._conservative_bot = ConservativeStrategyBot(*args, **kwargs)
        self._aggressive_bot = AggressiveStrategyBot(*args, **kwargs)


    # overridden
    def callback_receiver(self, prev_turn):
        if TemplateBot.exclude_trivialities(self, prev_turn):
            return
        winning_strategy = random.randint(1,3)
        print(winning_strategy)
        #if winning_strategy == 0:
            #accuse.callback_receiver(self, prev_turn)
        if winning_strategy == 1:
            self._random_bot.callback_receiver(prev_turn)
        elif winning_strategy == 2:
            self._conservative_bot.callback_receiver(prev_turn)
        elif winning_strategy == 3:
            self._aggressive_bot.callback_receiver(prev_turn)


if __name__ == "__main__":
    bot = CombineStrategyBot("combine_bot")
    bot.run()
