from duckling.bots.strategies import WeightedDistributionMLStrategy
from duckling.bots.strategy_bot import StrategyBot

if __name__ == "__main__":
    bot = StrategyBot("ups789", WeightedDistributionMLStrategy(model="model_30_09_2020_13_58_23"))
    bot.run()
