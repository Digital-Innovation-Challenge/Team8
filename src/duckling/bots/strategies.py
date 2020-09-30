import random

import duckling.lib.tools as tools


class AbstractStrategy:
    """
    This is an abstract strategy taking care of the trivialities. To use a strategy, create a StrategyBot using it.
    To create a more sophisticated strategy, extend this class and override the functions should_accuse_non_trivially
    and announce.
    """

    def should_accuse(self, prev_turns):
        """
        Returns whether or not the bot should accuse including trivial cases.
        :param prev_turns: The previous turns as a list of 2-tuples containing the player and the announced roll
        :return: True if the bot should accuse, False otherwise
        """
        if prev_turns is None or len(prev_turns) == 0:
            return False
        elif prev_turns[-1][1] == (2, 1):
            return True
        else:
            return self.should_accuse_non_trivially(prev_turns)

    def should_accuse_non_trivially(self, prev_turns):
        """
        Override this function to decide whether to accuse in non-trivial cases
        :param prev_turns: The previous turns as a list of 2-tuples containing the player and the announced roll
        :return: True if the bot should accuse, False otherwise
        """
        pass

    def announce(self, prev_turns, our_roll):
        """
        Override this function to decide what to announce
        :param prev_turns: The previous turns as a list of 2-tuples containing the player and the announced roll
        :param our_roll: Our current hidden roll as a 2-tuple
        :return: The roll we should announce as a 2-tuple
        """
        pass


class RandomStrategy(AbstractStrategy):

    def __init__(self, accuse_percentage=0.1):
        self.accuse_percentage = accuse_percentage

    def should_accuse_non_trivially(self, prev_turn):
        return random.random() < self.accuse_percentage

    def announce(self, prev_turn, our_roll):
        all_values = tools.valid_game_values_lowest_to_highest()
        if prev_turn is None:
            values_to_choose_from = all_values
        else:
            value = prev_turn[1]
            index = tools.value_to_rank(value)
            values_to_choose_from = all_values[index + 1:]
        announce_value = random.choice(values_to_choose_from)
        return announce_value


class AggressiveStrategy(AbstractStrategy):
    def should_accuse_non_trivially(self, prev_turns):
        return False

    def announce(self, prev_turns, our_roll):
        prev_roll = prev_turns[-1][1]
        rank = max(tools.value_to_rank((5, 4)), tools.value_to_rank(prev_roll) + 1, tools.value_to_rank(our_roll))
        return tools.rank_to_value(rank)
