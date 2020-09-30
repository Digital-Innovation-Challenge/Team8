from duckling.bots.strategies import MLStrategyFromOldStrategy, RandomStrategy
from duckling.bots.strategy_bot import StrategyBot

if __name__ == "__main__":
    bot = StrategyBot("ups123", MLStrategyFromOldStrategy(RandomStrategy(accuse_percentage=0.1),
                                                          "model_30_09_2020_13_58_23"))
    bot.run()
