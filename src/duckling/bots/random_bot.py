from duckling.bots.strategies import RandomStrategy
from duckling.bots.strategy_bot import StrategyBot

if __name__ == "__main__":
    bot = StrategyBot("true_random_bot", RandomStrategy(accuse_percentage=0.1))
    bot.run()
