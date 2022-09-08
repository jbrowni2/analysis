import os
import json
import matplotlib.pyplot as plt
from statistics import mean
import pandas as pd
import numpy as np
from scipy import stats, special
import matplotlib.colors as mcolors
from math import exp, sqrt, pi, erfc
from lmfit import Model
from scipy.optimize import curve_fit
from pygama import __version__ as pygama_version
import pygama
import pygama.lgdo as lgdo
import pygama.lgdo.lh5_store as lh5
from scipy.fft import fft, ifft, fftfreq
from os.path import expanduser
import copy

def findRms(array):
    rms = np.sqrt((np.mean(array[0:1000]**2)))
    return rms

def find_nearest_bin(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def get_peak(data, min, max):
    counts, bins, bars = plt.hist(data, histtype='step', bins=160000)

    peak_min, peak_max = min, max

    peak_range = find_nearest_bin(bins, peak_min), find_nearest_bin(bins, peak_max)

    peak_idx = np.argmax(counts[peak_range[0]:peak_range[1]]) + peak_range[0]

    peak = bins[peak_idx]

    return peak
