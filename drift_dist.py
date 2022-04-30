import foundation
from scipy.fft import fft, ifft, fftfreq
from pygama.dsp.build_processing_chain import *
import pygama.git as git
from pygama.utils import update_progress
from pygama.dsp.units import *
from pygama.dsp.ProcessingChain import ProcessingChain
from pygama import __version__ as pygama_version
from pygama import lh5
from scipy.optimize import curve_fit
from lmfit import Model
from math import exp, sqrt, pi, erfc
import matplotlib.colors as mcolors
from scipy import stats, special
import numpy as np
import pandas as pd
from statistics import mean
import matplotlib.pyplot as plt
import json
import os
import csv

with open("analysis.json", "r") as read_file:
    settings = json.load(read_file)

Ge_detector = settings['Drift Time']['Ge Channel']

with open("detectors.json", "r") as read_file:
    data = json.load(read_file)

slope = data[settings['detector']]['Calibration'][0]
intercept = data[settings['detector']]['Calibration'][1]

t2_noise = foundation.get_t2_data(settings['files'])

energycal = [element * slope + intercept for element in t2_noise['trapEmax'].nda]

drift = []

for i in range(1, len(t2_noise['tp_50'])):
    if energycal[i] <= 1000:
        if t2_noise['channel'].nda[i] == Ge_detector:
            time = (t2_noise['tp_50'].nda[i] - t2_noise['tp_50'].nda[i-1])*8
            if time >= 10000:
                drift.append(time)


#plt.rcParams['figure.facecolor'] = 'white'
plt.hist(data, histtype='step', bins=3000)
# plt.yscale('log')
plt.title("Preliminary Drift Time Measurement of Ge detector " + str(settings['detector']))
plt.xlabel("Time ns")
plt.ylabel("Counts")
# plt.ylim(0,100)
plt.xlim(0, 5000)
plt.show()
