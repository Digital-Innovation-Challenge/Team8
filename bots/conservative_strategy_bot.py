from lib.template_bot import TemplateBot
from lib.tools import probability_of_value_above, higher_than, rank_to_value, value_to_rank


class ConservativeStrategyBot(TemplateBot):
    """
    This bot accuses if the chance of rolling higher is below 50%. Otherwise it tells the truth or minimal lie.
    """

    # overridden
    def callback_receiver(self, prev_turn):
        if super(ConservativeStrategyBot, self).exclude_trivialities(prev_turn, first_turn=(5, 4)):
            return
        value = prev_turn[1]
        if probability_of_value_above(value) < 0.5:
            self.bot.accuse()
        else:
            roll = self.bot.roll()
            if higher_than(roll, value):
                announcement = roll
            else:
                announcement = rank_to_value(value_to_rank(value) + 1)
            self.bot.announce(announcement)


if __name__ == "__main__":
    bot = ConservativeStrategyBot("conservative_strategy")
    bot.run()
