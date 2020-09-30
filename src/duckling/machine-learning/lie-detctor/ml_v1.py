import yaml
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from duckling.lib.tools import *

data = None
X = [] 
Y = [] 

with open("/home/florian/Projekt/Team8/machine-learning/lie-detctor/mia_30-09-2020_01_26_21.yaml", 'r') as load_file:
    data = yaml.full_load(load_file)

# Person -1
# 1 neuron mit rank 22 values
# 1 neuron with prop
# 1 neuron with prop above

# Person -2
# 1 neuron mit rank 22 values
# 1 neuron with prop above
# 1 neuron with prop

# Deveriation
# 1 neuron differenz von 1 und 2 22 values

# Position
# 1 neuron with 0 - max player count

false_label = 0

for game in data:
    num_players = len(game['players'])
    for idx, move in enumerate(game['moves']):
        if move['lied'] is not None:
            # Person n
            val = move['announced']

            rank = float(1 + value_to_rank(val)) / 21
            prob = probability_of_value(val)
            prob_above = probability_of_value_above(val)

            # Person n - 1
            if idx - 1 >= 0:
                val_pre = game['moves'][idx - 1]['announced']
                rank_pre = float(1 + value_to_rank(val_pre)) / 22
                prob_pre = probability_of_value(val_pre)
                prob_above_pre = probability_of_value_above(val_pre)
            else:
                rank_pre = 0.0
                prob_pre = 0.0
                prob_above_pre = 1.0

            # Deveriation
            deveriation = rank - rank_pre

            # Position
            position = idx / 21

            # Label
            if move['lied']:
                label = [0.0, 1.0]
            else:
                label = [1.0, 0.0]
                false_label += 1

            #print(f"{rank:.2f}, {prob:.2f}, {prob_above:.2f}, {rank_pre:.2f}, {prob_pre:.2f}, {prob_above_pre:.2f}, {label}")

            X.append([rank, prob, prob_above, rank_pre, prob_pre, prob_above_pre])
            Y.append(label)


X = np.array(X)
Y = np.array(Y)

X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.3, random_state=42)

params = {
    "hidden_layer_sizes": (6,4),
    "activation": 'relu',
    "solver": 'sgd',
    "learning_rate": "constant",
    "learning_rate_init": 0.001,
    "batch_size": 8,
    "max_iter": 20000,
    "shuffle": True, 
    "random_state": 42, 
    "tol": 0.000001, 
    "verbose": 1, 
    "early_stopping": True,
    "validation_fraction": 0.2, 
    "n_iter_no_change": 100,
}

mlp = MLPClassifier(**params) # design your network

# Yes, it is still that easy to train a network
mlp.fit(X_train, Y_train)
print("Training set score: %f" % mlp.score(X_train, Y_train))
print("Test set score: %f" % mlp.score(X_test, Y_test))
print(false_label/len(Y))

