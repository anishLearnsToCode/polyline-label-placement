import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
from math import sqrt

START_VAL = 0.3
END_VAL = 0.7
DIFFERENCE = END_VAL - START_VAL
EPSILON= 1e-6

plt.rcParams['xtick.bottom'] = plt.rcParams['xtick.labelbottom'] = False
plt.rcParams['xtick.top'] = plt.rcParams['xtick.labeltop'] = True
plt.gca().invert_yaxis()
plt.ylabel('Y-Axis')
plt.title('X-Axis')


def plot_polyline_and_label(X, Y, label_x, label_y, label_position='top-right'):
    plt.plot(X, Y)
    plot_label(label_x, label_y, label_position)


def plot_label(x, y, placement='top-right'):
    if placement == 'top-right':
        plot_label_top_right(x, y)
    elif placement == 'bottom-right':
        plot_label_bottom_right(x, y)
    elif placement == 'top-left':
        plot_label_top_left(x, y)
    elif placement == 'bottom-left':
        plot_label_bottom_left(x, y)


def plot_label_position(x, y, x_shift, y_shift):
    plt.plot([x, x], [y, y + y_shift], color='black')
    plt.plot([x, x + x_shift], [y + y_shift, y + y_shift], color='black')
    plt.plot([x + x_shift, x + x_shift], [y + y_shift, y], color='black')
    plt.plot([x + x_shift, x], [y, y], color='black')


def plot_label_bottom_right(x, y):
    plot_label_position(x, y, 100, 50)


def plot_label_top_right(x, y):
    plot_label_position(x, y, 100, -50)


def plot_label_bottom_left(x, y):
    plot_label_position(x, y, -100, 50)


def plot_label_top_left(x, y):
    plot_label_position(x, y, -100, -50)


def distance(x1, y1, x2, y2) -> float:
    dx = x2 - x1
    dy = y2 - y1
    return sqrt(dx ** 2 + dy ** 2)


def binary_search(array, x) -> int:
    left, right, middle = 0, len(array) - 1, 0
    while left <= right:
        middle = left + (right - left) // 2
        if array[middle] == x: return middle
        elif array[middle] > x: right = middle - 1
        else: left = middle + 1
    return left


def get_position_from_vector(slope) -> str:
    if slope > 0: return np.random.choice(['top-right', 'bottom-left'])
    return np.random.choice(['top-left', 'bottom-right'])


if __name__ == '__main__':
    X_datum, Y_datum = [], []
    with open('data_1.txt') as file:
        for line in file.readlines():
            X, Y = [], []
            for i, point in enumerate(line.strip().split()):
                if i % 2 == 0:
                    X.append(int(point))
                else:
                    Y.append(int(point))
            X_datum.append(X)
            Y_datum.append(Y)

    no_of_polylines = len(X_datum)
    increment = 0.2 if no_of_polylines == 1 else DIFFERENCE / (no_of_polylines - 1)
    labels = []

    for i, (X, Y) in enumerate(zip(X_datum, Y_datum)):
        distances = []
        for j in range(1, len(X)):
            distances.append((0 if len(distances) == 0 else distances[-1]) + distance(X[j - 1], Y[j - 1], X[j], Y[j]))
        total_distance = distances[-1]
        label_point_distance = (START_VAL + i * increment) * total_distance
        segment_index = binary_search(distances, label_point_distance)

        previous_distance = (0 if segment_index == 0 else distances[segment_index - 1])
        extra_distance = label_point_distance - previous_distance
        segment_length = distances[segment_index] - previous_distance
        ratio = extra_distance / (distances[segment_index] - previous_distance)
        slope = (Y[segment_index + 1] - Y[segment_index] + EPSILON) / (X[segment_index + 1] - X[segment_index] + EPSILON)
        label_y = Y[segment_index] + segment_length * ratio * slope / sqrt(slope ** 2 + 1)
        label_x = X[segment_index] + segment_length * ratio / sqrt(slope ** 2 + 1)
        label = (label_x, label_y, get_position_from_vector(slope))
        labels.append(label)
        print(label)
        plot_polyline_and_label(X, Y, label_x, label_y, label[-1])
    plt.show()
