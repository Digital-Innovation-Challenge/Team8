import random

import duckling.lib.tools as tools
from duckling.machine_learning.lie_detctor.lie_detector import InferenceEngine
from numpy.random import binomial


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
        Call this function to find out what to announce
        :param prev_turns: The previous turns as a list of 2-tuples containing the player and the announced roll
        :param our_roll: Our current hidden roll as a 2-tuple
        :return: The roll we should announce as a 2-tuple
        """
        if prev_turns is None or len(prev_turns) == 0:
            return self.announce_first_turn(our_roll)
        else:
            return self.announce_later_turn(prev_turns, our_roll)

    def announce_first_turn(self, our_roll):
        """
        Override this function to decide what to announce on the first turn
        :param our_roll: Our current hidden roll as a 2-tuple
        :return: The roll we should announce as a 2-tuple
        """
        pass

    def announce_later_turn(self, prev_turns, our_roll):
        """
        Override this function to decide what to announce after the first turn
        :param prev_turns: The previous turns as a list of 2-tuples containing the player and the announced roll
        :param our_roll: Our current hidden roll as a 2-tuple
        :return: The roll we should announce as a 2-tuple
        """
        pass


class AbstractMLStrategy(AbstractStrategy):
    """
    Implementation of AbstractStrategy using a given machine learning model
    """

    def __init__(self, model, version=0):
        super(AbstractStrategy, self).__init__()
        self._detector_ie = InferenceEngine(model, version=version)
        self._version = version

    # overridden
    def should_accuse_non_trivially(self, prev_turns):
        classifier_data = {
            'val': prev_turns[-1][1]
        }
        if self._version == 1:
            classifier_data['position'] = len(prev_turns) + 1
        if len(prev_turns) > 1:
            classifier_data['val_pre'] = prev_turns[-2][1]

        print(classifier_data)

        accuse = self._detector_ie.inference(classifier_data)
        return accuse


class MLStrategyFromOldStrategy(AbstractMLStrategy):
    def __init__(self, old_strategy, model, version=0):
        super(AbstractMLStrategy, self).__init__()
        self._detector_ie = InferenceEngine(model, version=version)
        self._version = version
        self.old_strategy = old_strategy

    def announce(self, prev_turns, our_roll):
        return self.old_strategy.announce(prev_turns, our_roll)


class RandomStrategy(AbstractStrategy):

    def __init__(self, accuse_percentage=0.1):
        self.accuse_percentage = accuse_percentage

    def should_accuse_non_trivially(self, prev_turns):
        return random.random() < self.accuse_percentage

    def announce_first_turn(self, our_roll):
        return random.choice(tools.valid_game_values_lowest_to_highest())

    def announce_later_turn(self, prev_turns, our_roll):
        all_values = tools.valid_game_values_lowest_to_highest()
        prev_roll = prev_turns[-1][1]
        value = prev_roll
        index = tools.value_to_rank(value)
        higher_values = all_values[index + 1:]
        announce_value = random.choice(higher_values)
        return announce_value


class AggressiveStrategy(AbstractStrategy):
    def should_accuse_non_trivially(self, prev_turns):
        return False

    def announce_first_turn(self, our_roll):
        rank = max(tools.value_to_rank((5, 4)), tools.value_to_rank(our_roll))
        return tools.rank_to_value(rank)

    def announce_later_turn(self, prev_turns, our_roll):
        prev_roll = prev_turns[-1][1]
        rank = max(tools.value_to_rank((5, 4)), tools.value_to_rank(prev_roll) + 1, tools.value_to_rank(our_roll))
        return tools.rank_to_value(rank)


class ConservativeStrategy(AbstractStrategy):
    def should_accuse_non_trivially(self, prev_turns):
        if tools.higher_than((5, 4), prev_turns):
            return False
        return True

    def announce_first_turn(self, our_roll):
        return our_roll

    def announce_later_turn(self, prev_turns, our_roll):
        if tools.higher_than(our_roll, prev_turns[-1][1]):
            announcement = our_roll
        else:
            announcement = tools.rank_to_value(tools.value_to_rank(prev_turns[-1][1]) + 1)
        return announcement


class BinomialDistributionMLStrategy(AbstractMLStrategy):
    def __init__(self, *args, **kwargs):
        super(BinomialDistributionMLStrategy, self).__init__(*args[1:], **kwargs)
        self.p = args[0]

    def announce_first_turn(self, our_roll):
        return our_roll

    def announce_later_turn(self, prev_turns, our_roll):
        our_rank = tools.value_to_rank(our_roll)
        prev_rank = tools.value_to_rank(prev_turns[-1][1])
        if our_rank > prev_rank:
            return our_roll
        else:
            n = 21 - prev_rank
            top_by = binomial(n, self.p)
            return tools.rank_to_value(prev_rank + top_by)


class WeightedDistributionMLStrategy(AbstractMLStrategy):
    def __init__(self, *args, **kwargs):
        super(WeightedDistributionMLStrategy, self).__init__(*args[1:], **kwargs)

    def announce_first_turn(self, our_roll):
        return our_roll

    def announce_later_turn(self, prev_turns, our_roll):
        our_rank = tools.value_to_rank(our_roll)
        prev_rank = tools.value_to_rank(prev_turns[-1][1])
        if our_rank > prev_rank:
            return our_roll
        else:
            higher_values = tools.valid_game_values_lowest_to_highest()[prev_rank + 1:]
            weights = [tools.probability_of_value(value) for value in higher_values]
            return random.choices(higher_values, weights=weights)[0]
