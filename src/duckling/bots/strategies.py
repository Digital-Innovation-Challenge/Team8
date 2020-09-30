import random
import random_bot
import always_accuse_bot
import aggressive_strategy_bot
import conservative_strategy_bot
import duckling.lib.tools as tools
from duckling.bots.template_bot import TemplateBot
accuse_percentage = 0.1

class RandomStrategy():

    def trivialities(self, prev_turn):
        if TemplateBot.exclude_trivialities(self, prev_turn):
            return

    def should_accuse(self):
        accuse = random.random() < accuse_percentage
        return accuse

    def announce(self, prev_turn):
        all_values = tools.valid_game_values_lowest_to_highest()
        if prev_turn is None:
            values_to_choose_from = all_values
        else:
            value = prev_turn[1]
            index = tools.value_to_rank(value)
            values_to_choose_from = all_values[index + 1:]
        announce_value = random.choice(values_to_choose_from)
        return announce_value

class AggressiveStrategy(): 

    def should_accuse(self):
        return None
    
    def announce(self, prev_turn):
        return None

class ConservativeStrategy():
    def callback_receiver(self, prev_turn):
        return None


