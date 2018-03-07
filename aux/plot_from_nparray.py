import numpy as np
from pylab import *
from collections import Counter


def plot_and_show_cdf(arr, theta=1.0, style="r", label=None):
    cntr =Counter(arr)
    x, y = zip(*sorted(cntr.iteritems()))
    y = map(float, y)
    x = np.asarray(x)
    y = np.asarray(y)
    y /= y.sum()
    if theta < 1.0:
        new_len = sum(x < theta)
        x = x[:new_len]
        y = y[:new_len]
    cum_y = np.cumsum(y)
    plot(x, cum_y, style, label=label)
    show()

def plot_cdf(arr, theta=1.0, style="r", label=None):
    cntr =Counter(arr)
    x, y = zip(*sorted(cntr.iteritems()))
    y = map(float, y)
    x = np.asarray(x)
    y = np.asarray(y)
    y /= y.sum()
    if theta < 1.0:
        new_len = sum(x < theta)
        x = x[:new_len]
        y = y[:new_len]
    cum_y = np.cumsum(y)
    plot(x, cum_y, style, label=label)

def array_to_cdf(arr, theta=1.0):
    cntr =Counter(arr)
    x, y = zip(*sorted(cntr.iteritems()))
    y = map(float, y)
    x = np.asarray(x)
    y = np.asarray(y)
    y /= y.sum()
    if theta < 1.0:
        new_len = sum(x < theta)
        x = x[:new_len]
        y = y[:new_len]
    cum_y = np.cumsum(y)
    return x, cum_y