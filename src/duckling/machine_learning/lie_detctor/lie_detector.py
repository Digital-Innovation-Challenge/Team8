import pickle
import pathlib
import numpy as np
from duckling.lib.tools import *
from sklearn.neural_network import MLPClassifier
from duckling.lib.tools import *

class InferenceEngine(object):
    def __init__(self, model=None, version=0):
        """
        Executes the ML lie detector.

        :param model: Name of the model
        :param version: Version of the model architecture
        """
        self.model_version = 0
        self._policy = None
        if model is not None:
            model_folder = (pathlib.Path(__file__).parent / pathlib.Path(model + ".pickle")).absolute()
            self.load_model(model_folder)

    def load_model(self, filename):
        """
        Explicitly loads a model file.
        """
        print(f"Requested model {filename}\nLoading model...")
        with open(filename, "rb") as handle:
            self._policy = pickle.load(handle)

    def inference(self, data):
        """
        Executes the model on given data.
        :param data: 
            Version 0:
                A dict containing the value tuples of the previous players name 'val' and 'val_pre'
        :return: 
            Version 0:
                The lie estimation as a boolean
        """
        if self.model_version == 0:
            # Generate and normalize classifyer inputs

            # Person n -1
            val = data['val']
            rank = float(1 + value_to_rank(val)) / 21
            prob = probability_of_value(val)
            prob_above = probability_of_value_above(val)
            # Person n - 2
            if 'val_pre' in data:
                val_pre = data['val_pre']
                rank_pre = float(1 + value_to_rank(val_pre)) / 22
                prob_pre = probability_of_value(val_pre)
                prob_above_pre = probability_of_value_above(val_pre)
            else:
                rank_pre = 0.0
                prob_pre = 0.0
                prob_above_pre = 1.0

            # Exec the network
            data = [rank, prob, prob_above, rank_pre, prob_pre, prob_above_pre]
            output = self._policy.predict([data])[0]
            print(output)
            if output[0] < 0.5:
                return True
            else:
                return False
        else:
            print("Unknown model version: {}".format(self.model_version))


if __name__ == "__main__":
    infe = InferenceEngine("model_30_09_2020_12_40_14")
    print(infe.inference({ 'val': (6,6), 'val_pre': (2,2)}), "{ 'val': (6,6), 'val_pre': (2,2)}")
