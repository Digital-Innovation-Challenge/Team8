from duckling.bots.strategies import BinomialDistributionMLStrategy
from duckling.bots.strategy_bot import StrategyBot

if __name__ == "__main__":
    bot = StrategyBot("ups456", BinomialDistributionMLStrategy(1 / 3, model="model_30_09_2020_13_58_23"))
    bot.run()
