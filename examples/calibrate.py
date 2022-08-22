import numpy as np
import pandas as pd
from statistics import mean
from scipy import stats
import matplotlib.pyplot as plt
import json
import os
import processes.foundation as fd
import processes.fitModel as fM
import processes.histogramAction as hA
import plotly.express as px
import sys

def main():
    peaks = [[80000,120000], [300000, 340000], [340000, 380000], [400000, 440000], [440000, 480000]]
    peak1_min, peak1_max = 80000,120000
    peak2_min, peak2_max = 300000, 340000
    peak3_min, peak3_max = 340000, 380000
    peak4_min, peak4_max = 400000, 440000
    peak5_min, peak5_max = 440000, 480000
    energy = [81.0, 276.40, 302.85, 356.02, 383.85]
    #processes.calibration.Calibrate(1034, 'BeGe', peaks = peaks, energy= energy)
    cwd = os.getcwd()
    file = cwd + '/detectors.json'
    #with open(file, "r") as read_file:
    #    detectors = json.load(read_file)

    adc = []
    runs = 1034

    if isinstance(runs, int):
        data = fd.get_df(runs)
    else:
        data = fd.get_df_multiple(runs)


    counts, bins, bars = plt.hist(data["trapEmax"], histtype='step', bins=160000)

    for range in peaks:
        peak_range = processes.foundation.find_nearest_bin(bins, range[0]), processes.foundation.find_nearest_bin(bins, range[1])
        peak_idx = np.argmax(counts[peak_range[0]:peak_range[1]] + peak_range[0])
        peak = bins[peak_idx]
        adc.append(peak)


    plt.yscale('log')
    plt.xlim(0, 70000)

    plt.axvline(x=peak1_min, color='r')
    plt.axvline(x=peak1_max, color='r')
    plt.axvline(x=peak2_min, color='green')
    plt.axvline(x=peak2_max, color='g')
    plt.axvline(x=peak3_min, color='r')
    plt.axvline(x=peak3_max, color='r')
    plt.axvline(x=peak4_min, color='green')
    plt.axvline(x=peak4_max, color='g')
    plt.axvline(x=peak5_min, color='green')
    plt.axvline(x=peak5_max, color='g')

    slope, intercept, r_value, p_value, std_err = stats.linregress(adc,energy)

    plt.show()

    print(slope)
    print(intercept)

    detectors = {"BeGe": {
                "Calibration": [slope, intercept]
            }
        }

    with open(file, "w") as file:
        json.dump(detectors,file, indent=6)


if __name__ == "__main__":
    main()
