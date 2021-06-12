from numpy.core.numeric import tensordot
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import sklearn.model_selection


def read_data_from_file():
    """
    read data from sample file
    :return:
    """
    return pd.read_csv('rectangle.txt', delim_whitespace=True, names=['x_val', 'y_val', 'label'])


def split_data(data, target):
    """
    Split dataset into training set and test set
    :param data: pandas data frame contains the data
    :return: train set, test set data frames
    """
    return sklearn.model_selection.train_test_split(data, target, test_size=0.5)

# calculate the Euclidean distance between two vectors wwith given p


def euclidean_distance(row1, row2, p):

    distance = 0.0
    for i in range(len(row1)-1):
        distance += (row1[i] - row2[i])**p
    return distance**(1/p)


# Locate the most similar neighbors
def get_neighbors(train, test_row, num_neighbors, p):

    distances = list()

    for train_row in train.itertuples():
        dist = euclidean_distance(test_row, train_row, p)
        distances.append((train_row, dist))
    distances.sort(key=lambda tup: tup[1])
    neighbors = list()
    for i in range(num_neighbors):
        neighbors.append(distances[i][0])
    return neighbors


# Make a classification prediction with neighbors
def predict_classification(train, test_row, num_neighbors, p):
    neighbors = get_neighbors(train, test_row, num_neighbors, p)
    output_values = [row.label for row in neighbors]
    prediction = max(set(output_values), key=output_values.count)
    return prediction


# kNN Algorithm
def k_nearest_neighbors(train, test, num_neighbors, p):
    predictions = list()

    for row in test.itertuples():

        output = predict_classification(train, row, num_neighbors, p)
        predictions.append(output)
    return predictions

# Calculate accuracy percentage


def accuracy_metric(actual, predicted):
    correct = 0

    for i in range(len(actual)-1):
        if actual[i] == predicted[i]:
            correct += 1
    return correct / float(len(actual)) * 100.0


def print_results(true_error_dict, empirical_error_dict):
    for x in true_error_dict:
        print("True error avg:",
              true_error_dict[x]/100, "Empirical error avg:", empirical_error_dict[x]/100)


def runner():
    data = read_data_from_file()
    true_error_avarage = {}
    empirical_error_avarage = {}

    for i in range(100):
        X_train, X_test, y_train, y_test = split_data(data, data['label'])

        for k in range(1, 10, 2):

            for p in [1, 2, float('inf')]:

                predicted_for_test = k_nearest_neighbors(X_train, X_test, k, p)
                predicted_for_train = k_nearest_neighbors(
                    X_train, X_train, k, p)

                true_error = 100 - \
                    accuracy_metric(y_test.tolist(), predicted_for_test)
                empirical_error = 100 - \
                    accuracy_metric(y_train.tolist(), predicted_for_train)

                if (i == 0):
                    true_error_avarage["{},{}".format(p, k)] = true_error
                    empirical_error_avarage["{},{}".format(
                        p, k)] = empirical_error

                else:

                    res_t = true_error_avarage.get(
                        "{},{}".format(p, k)) + true_error
                    res_e = empirical_error_avarage.get(
                        "{},{}".format(p, k)) + empirical_error
                    true_error_avarage.update({"{},{}".format(p, k): res_t})
                    empirical_error_avarage.update(
                        {"{},{}".format(p, k): res_e})

    print_results(true_error_avarage, empirical_error_avarage)


if __name__ == "__main__":
    runner()
