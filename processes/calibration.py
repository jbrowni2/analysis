import numpy as np
import pandas as pd
from statistics import mean
from scipy import stats
import matplotlib.pyplot as plt
import json
import os
from .foundation import *


def Calibrate(runs, det, peaks = None, energy = None):
    cwd = os.getcwd()
    file = cwd + '/detectors.json'
    #with open(file, "r") as read_file:
    #    detectors = json.load(read_file)

    adc = []

    if isinstance(runs, int):
        data = get_df(runs)
    else:
        data = get_df_multiple(runs)


    counts, bins, bars = plt.hist(data["trapEmax"], histtype='step', bins=160000)

    for range in peaks:
        peak_range = find_nearest_bin(bins, range[0]), find_nearest_bin(bins, range[1])
        peak_idx = np.argmax(counts[peak_range[0]:peak_range[1]] + peak_range[0])
        peak = bins[peak_idx]
        adc.append(peak)

    adc.sort()
    energy.sort()

    slope, intercept, r_value, p_value, std_err = stats.linregress(adc,energy)

    detectors = {det: {
                "Calibration": [slope, intercept]
            }
        }

    with open(file, "w") as file:
        json.dump(detectors,file, indent=6)
