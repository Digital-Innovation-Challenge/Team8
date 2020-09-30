import argparse
from duckling.bots.strategy_bot import StrategyBot
from duckling.bots.strategies import RandomStrategy, AggressiveStrategy, ConservativeStrategy, BinomialDistributionMLStrategy, WeightedDistributionMLStrategy, MLStrategyFromOldStrategy

"""
Wellcome to the duckling bot launcher!

Use 'python3 bot.py -h' to learn more.
"""

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Start some Bot')
    parser.add_argument('type', type=str, help='The name of the strategy. (agressive, binomial, conservative, weighted_dist, random)')
    parser.add_argument('name', type=str, help='The bots name')
    parser.add_argument('--ml', action='store_true', help='Should the machine learning lie detector be used')

    args = parser.parse_args()

    model = "model_30_09_2020_13_58_23"

    if args.type == "agressive":
        if args.ml:
            bot = StrategyBot(args.name, MLStrategyFromOldStrategy(AggressiveStrategy(), model))
        else:
            bot = StrategyBot(args.name, AggressiveStrategy())
    elif args.type == "binomial":
        if args.ml:
            bot = StrategyBot(args.name, BinomialDistributionMLStrategy(0.3, model))
        else:
            print("Binominial is only available for the ml strategy")
    elif args.type == "weighted_dist":
        if args.ml:
            bot = StrategyBot(args.name, WeightedDistributionMLStrategy(model=model))
        else:
            print("Weighted dist is only available for the ml strategy")
    elif args.type == "random":
        if args.ml:
            bot = StrategyBot(args.name, MLStrategyFromOldStrategy(RandomStrategy(accuse_percentage=0.1), model))
        else:
            bot = StrategyBot(args.name, RandomStrategy(accuse_percentage=0.1)) 
    elif args.type == "conservative":
        if args.ml:
            bot = StrategyBot(args.name, MLStrategyFromOldStrategy(ConservativeStrategy(), model))
        else:
            bot = StrategyBot(args.name, ConservativeStrategy())

    bot.run()
