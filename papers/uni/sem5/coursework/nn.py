import numpy as np
from sklearn.cluster import KMeans
from data import DataParser
import matplotlib.pyplot as plt
import pandas as pd
from itertools import permutations 
import tensorflow as tf

import warnings
warnings.filterwarnings('ignore')


def main():
    labels = np.load("mus_labels.npy")
    samples = np.load(f"mus_samples.npy", allow_pickle=True)
    test_labels = np.load("test_labels.npy")
    test_samples = np.load(f"test_samples.npy", allow_pickle=True)

    kmeans = KMeans(n_clusters=4)
    kmeans.fit(samples)
    predicted_labels = kmeans.predict(test_samples)

    perms = permutations([0, 1, 2, 3]) 

    rate = 0
    mapping = {}
    for perm in perms:
        new_mapping = {index: value for (index, value) in enumerate(perm)}
        correct = sum([1 if test_label == new_mapping[label] else 0 for (test_label, label) in zip(test_labels, predicted_labels)])
        new_rate = correct / len(test_labels)
        if new_rate > rate:
            rate = new_rate
            mapping = new_mapping

    print(rate)
    print(list(test_labels))
    print([mapping[label] for label in predicted_labels])


    model = tf.keras.Sequential([ tf.keras.layers.Flatten(input_shape=(193,)), tf.keras.layers.Dense(128, activation='relu'), tf.keras.layers.Dense(4) ])
    model.compile(optimizer='adam', loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=['accuracy'])
    model.fit(samples, labels, epochs=20)
    test_loss, test_acc = model.evaluate(test_samples,  test_labels)
    print('\nTest accuracy:', test_acc)


if __name__ == "__main__":
    main()
