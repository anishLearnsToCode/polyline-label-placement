import sys
from math import sqrt
from typing import List, Union

import matplotlib.pyplot as plt
import numpy as np

# start value and end value are the ratios in which all labels will be plotted, eg. if
# the pair is (0.3, 0.8) that means that all label points will be created between 0.3
# and 0.8 of every poly-line.

# If the pair value is (0.4, 0.6) then all labels will be created around the center of
# every polyline, whereas if the difference is larger labels will be more spread out and
# all of them might not be near the center
START_VAL = 0.3
END_VAL = 0.7
DIFFERENCE = END_VAL - START_VAL

# epsilon is a very small value created for use in mathematical calculations where
# there is a fear of division by 0. This helps us against that by dividing by very small
# value instead but still giving a very large number
EPSILON = 1e-6

# Boilerplate code to set the axes of the graph
plt.rcParams['xtick.bottom'] = plt.rcParams['xtick.labelbottom'] = False
plt.rcParams['xtick.top'] = plt.rcParams['xtick.labeltop'] = True
plt.gca().invert_yaxis()
plt.ylabel('Y-Axis')
plt.title('X-Axis')


def plot_polyline_and_label(X: List[int], Y: List[int], label_x: float, label_y: float, label_position='top-right'):
    """
    :param X list of x coordinates of polyline
    :param Y list of y coordinates of polyline
    :param label_x x coordinate of label
    :param label_y y coordinate of label
    :param label_position Position of label on the polyline repesented as a string
    This function draws the polyline on the common plot and also draws the bounding box
    for the label at the label's coordinates and with given position of size (100, 50)
    """
    plt.plot(X, Y)
    plot_label(label_x, label_y, label_position)


def plot_label(x, y, placement='top-right'):
    """
    :param x x coordinate of label
    :param y y coordinate of label
    :param placement string representing the position of label box with respect to polyline
    """
    if placement == 'top-right':
        plot_label_top_right(x, y)
    elif placement == 'bottom-right':
        plot_label_bottom_right(x, y)
    elif placement == 'top-left':
        plot_label_top_left(x, y)
    elif placement == 'bottom-left':
        plot_label_bottom_left(x, y)


def plot_label_position(x: float, y: float, x_shift: float, y_shift: float):
    """
    :param x x coordinate of label
    :param y y coordinate of label
    :param x_shift shift value representing the label bounding box dimensions in x axis
    :param y_shift shift value representing the label bounding box dimensions in y axis
    """
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
    """
    :param x1 x coordinate of first point
    :param x2 x coordinate of second point
    :param y1 y coordinate of first point
    :param y2 y coordinate of second point
    :return distance between 2 points
    """
    dx = x2 - x1
    dy = y2 - y1
    return sqrt(dx ** 2 + dy ** 2)


def binary_search(array: List[float], x: float) -> int:
    """
    :param array list of numbers in sorted order
    :param x element to find
    :return index of matching element or larger element
    """
    left, right, middle = 0, len(array) - 1, 0
    while left <= right:
        middle = left + (right - left) // 2
        if array[middle] == x:
            return middle
        elif array[middle] > x:
            right = middle - 1
        else:
            left = middle + 1
    return left


def get_position_from(slope) -> str:
    """
    :param slope slope of line segment where the label is being drawn
    :return returns position of label bounding box  
    """
    if slope > 0: return np.random.choice(['top-right', 'bottom-left'])
    return np.random.choice(['top-left', 'bottom-right'])


if __name__ == '__main__':
    X_datum, Y_datum = [], []
    with open(sys.argv[1]) as file:
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
        slope = (Y[segment_index + 1] - Y[segment_index] + EPSILON) / (
                    X[segment_index + 1] - X[segment_index] + EPSILON)
        label_y = Y[segment_index] + segment_length * ratio * slope / sqrt(slope ** 2 + 1)
        label_x = X[segment_index] + segment_length * ratio / sqrt(slope ** 2 + 1)
        label = (label_x, label_y, get_position_from(slope))
        labels.append(label)
        print(label)
        plot_polyline_and_label(X, Y, label_x, label_y, label[-1])
    plt.show()
