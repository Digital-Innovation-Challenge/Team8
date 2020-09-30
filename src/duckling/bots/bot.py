import argparse
from duckling.bots.strategy_bot import StrategyBot
from duckling.bots.strategies import RandomStrategy, AggressiveStrategy, BinomialDistributionMLStrategy, MLStrategyFromOldStrategy

"""
Wellcome to the duckling bot launcher!

Use 'python3 bot.py -h' to learn more.
"""

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Start some Bot')
    parser.add_argument('type', type=str, help='The name of the strategy. (agressive, binomial, random)')
    parser.add_argument('name', type=str, help='The bots name')
    parser.add_argument('--ml', action='store_true', help='Should the machine learning lie detector be used')

    args = parser.parse_args()

    if args.type == "agressive":
        if args.ml:
            bot = StrategyBot(args.name, MLStrategyFromOldStrategy(AggressiveStrategy(), "model_30_09_2020_13_58_23"))
        else:
            bot = StrategyBot(args.name, AggressiveStrategy())
    if args.type == "binomial":
        if args.ml:
            bot = StrategyBot(args.name, BinomialDistributionMLStrategy(0.3, "model_30_09_2020_13_58_23"))
        else:
            print("binominial is only available for the ml strategy")
    if args.type == "random":
        if args.ml:
            bot = StrategyBot(args.name, MLStrategyFromOldStrategy(RandomStrategy(accuse_percentage=0.1), "model_30_09_2020_13_58_23"))
        else:
            bot = StrategyBot(args.name, RandomStrategy(accuse_percentage=0.1))    

    bot.run()
