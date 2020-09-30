from duckling.bots.strategies import AggressiveStrategy
from duckling.bots.strategy_bot import StrategyBot

if __name__ == "__main__":
    bot = StrategyBot("true_random_bot", AggressiveStrategy())
    bot.run()
