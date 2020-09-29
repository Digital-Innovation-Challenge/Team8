def valid_game_values_lowest_to_highest():
    """
    Gives a list of the 21 valid game values ordered from lowest to highest.
    """
    return [(3, 1), (3, 2), (4, 1), (4, 2), (4, 3), (5, 1), (5, 2), (5, 3), (5, 4), (6, 1), (6, 2), (6, 3), (6, 4),
            (6, 5), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (2, 1)]


def value_to_rank(value):
    """
    Converts a game value to its rank. Lower ranks correspond to lower game values.

    :param value: A rank as an integer 0, 1, ..., 20
    :returns: The corresponding game value as a tuple
    :raises: ValueError if value is not a valid game value
    """
    index = valid_game_values_lowest_to_highest().index(value)
    if index == -1:
        raise ValueError("Not a valid game value")
    return index


def rank_to_value(rank):
    """
    Converts a value rank to its game value. Lower game values correspond to lower ranks.

    :param rank: A rank as an integer 0, 1, ..., 20
    :returns: The corresponding game value
    :raises: ValueError if rank is not a valid rank
    """
    if rank not in range(21):
        raise ValueError("Not a valid game rank. Valid ranks are integers 0, 1, ..., 20")
    return valid_game_values_lowest_to_highest()[rank]


def higher_than(value1, value2):
    """
    Checks whether value1 is higher than value2 as a game value.

    :param value1: A valid game value as a 2-tuple
    :param value2: Another valid game value as a 2-tuple
    :returns: True if and only if value1 is higher than value2 as a game value.
    """
    return value_to_rank(value1) > value_to_rank(value2)


def probability_of_value(value, use_rank=False):
    """
    Gives the probability of rolling the given game value.

    :param value: A valid game value as a 2-tuple
    :param use_rank: Set True to use a rank not a 2-tuple
    :returns: The probability of the value occurring on any given roll.
    """
    # convert to value if using rank
    if use_rank:
        value = rank_to_value(value)

    return 1 / 36 if (value[0] * 10 + value[1]) % 11 == 0 else 1 / 18
