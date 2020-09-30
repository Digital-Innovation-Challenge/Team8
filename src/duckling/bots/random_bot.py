import random

import duckling.lib.tools as tools
from duckling.bots.template_bot import TemplateBot
from duckling.machine_learning.lie_detctor.lie_detector import InferenceEngine 

accuse_percentage = 0.1


class RandomBot(TemplateBot):
    """
    This bot decides randomly what action to take and in case of announcing what value to choose.
    """

    def __init__(self, *args, **kwargs):
        super(RandomBot, self).__init__(*args, **kwargs)
        
        self._detector_ie = InferenceEngine("model_30_09_2020_13_58_23")

    # overridden
    def callback_receiver(self, prev_turn):
        if TemplateBot.exclude_trivialities(self, prev_turn):
            return

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
            all_values = tools.valid_game_values_lowest_to_highest()
            if prev_turn is None:
                values_to_choose_from = all_values
            else:
                value = prev_turn[1]
                index = tools.value_to_rank(value)
                values_to_choose_from = all_values[index + 1:]

            self.bot.roll()
            announce_value = random.choice(values_to_choose_from)
            self.bot.announce(announce_value)


if __name__ == "__main__":
    bot = RandomBot("random_bot_with_ml")
    bot.run()
