from duckling.bots.template_bot import TemplateBot
from duckling.lib.tools import probability_of_value_above, higher_than, rank_to_value, value_to_rank
from duckling.machine_learning.lie_detctor.lie_detector import InferenceEngine 


class ConservativeStrategyBot(TemplateBot):
    """
    This bot accuses if the chance of rolling higher is below 50%. Otherwise it tells the truth or minimal lie.
    """

    def __init__(self, *args, **kwargs):
        super(ConservativeStrategyBot, self).__init__(*args, **kwargs)
        
        self._detector_ie = InferenceEngine("model_30_09_2020_13_58_23")


    # overridden
    def callback_receiver(self, prev_turn):
        if super(ConservativeStrategyBot, self).exclude_trivialities(prev_turn, first_turn=(5, 4)):
            return
        value = prev_turn[1]


        previous_plays = self.bot.get_announced()
        classifier_data = {
            'val': previous_plays[-1][1]
        }
        if len(previous_plays) > 1:
            classifier_data['val_pre'] = previous_plays[-2][1]

        print(classifier_data)

        accuse = self._detector_ie.inference(classifier_data)

        if accuse:
            self.bot.accuse()
        else:
            roll = self.bot.roll()
            if higher_than(roll, value):
                announcement = roll
            else:
                announcement = rank_to_value(value_to_rank(value) + 1)
            self.bot.announce(announcement)


if __name__ == "__main__":
    bot = ConservativeStrategyBot("cons_strategy_ml")
    bot.run()
