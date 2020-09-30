from duckling.bots.template_bot import TemplateBot
from duckling.lib.tools import rank_to_value, value_to_rank


class AggressiveStrategyBot(TemplateBot):
    """
    This bot always announces an aggressively high value.
    """

    # overridden
    def callback_receiver(self, prev_turn):
        if super(AggressiveStrategyBot, self).exclude_trivialities(prev_turn, first_turn=(5, 4)):
            return
        value = prev_turn[1]
        roll = self.bot.roll()
        rank = max(value_to_rank((5, 4)), value_to_rank(value) + 1, value_to_rank(roll))
        self.bot.announce(rank_to_value(rank))


if __name__ == "__main__":
    bot = AggressiveStrategyBot("aggressive_strategy")
    bot.run()
