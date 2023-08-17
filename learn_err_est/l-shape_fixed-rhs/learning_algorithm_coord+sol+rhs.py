import numpy as np
import multiprocessing
import os
import sys
sys.path.append('..')

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

from estimator_model import create_learn_predict

#set number of iterations
numiterations = 20

#load data
train_meshes = np.load("train_meshes.npy")
train_estimates = np.load("train_estimates.npy")
test_meshes = np.load("test_meshes.npy")
test_estimates = np.load("test_estimates.npy")

#calculate losses parallel
result = []
data = [[train_meshes, train_estimates, test_meshes, test_estimates]] * numiterations
pool_obj = multiprocessing.Pool()
result  = pool_obj.map(create_learn_predict, data)
pool_obj.close()
pool_obj.join()
losses = []
accuracies = []
for res in result:
    losses.append(res[0])
    accuracies.append(res[1])
print("----------------------------------------------------------------")
print("losses: ")
print(losses)
print("mean loss :", sum(losses)/len(losses))
print("accuracies:")
print(accuracies)
print("mean accuracy :", sum(accuracies)/len(accuracies))
np.save('losses_coord+sol+rhs',np.array(losses))
np.save('accuracies_coord+sol+rhs',np.array(accuracies))
print("losses and accuracies saved to file")
print("\007")
