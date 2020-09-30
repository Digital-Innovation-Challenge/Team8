from duckling.bots.template_bot import TemplateBot


class AlwaysAccuseBot(TemplateBot):
    """
    This bot always accuses except on the first turn where it announces the truth.
    """

    # overridden
    def callback_receiver(self, prev_turn):
        if prev_turn is None:
            roll = self.bot.roll()
            self.bot.announce(roll)
        else:
            self.bot.accuse()


if __name__ == "__main__":
    bot = AlwaysAccuseBot("always_accuse")
    bot.run()
