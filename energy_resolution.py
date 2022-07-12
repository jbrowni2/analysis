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


with open("address.json", "r") as read_file:
    data = json.load(read_file)

with open("analysis.json", "r") as read_file:
    settings = json.load(read_file)

slope = data[settings['detector']]['Calibration'][0]
intercept = data[settings['detector']]['Calibration'][1]

t2_noise = foundation.get_t2_data(settings['files'])

energycal = [element * slope + intercept for element in t2_noise['trapEmax'].nda]

peaks = settings['Energy Resolution']['peaks']

fwhm = []
en = []
error = []


for peak in peaks:
    fw, err, energy = foundation.get_fwhm(energycal, peak-10, peak+10, peak)
    fwhm.append(fw)
    en.append(energy)
    error.append(err)

m, intrcpt, c = foundation.energy_fit(fwhm, en, error)

x = np.arange(0, 1500, 0.1)
y = m*np.power(x + c*(np.power(x, 2)), 0.5) + intrcpt

plt.errorbar(en, fw, yerr=error, fmt='o')
plt.plot(x, y)
plt.title("Energy Resolution of Detector " + str(settings['detector']))
#plt.text(0,3.0, "Function is m*(E + c*(E^2)) + b")
#plt.text(1000,2.0,"m = 0.003")
#plt.text(1000,1.8,"c = 0.326")
#plt.text(1000,1.6,"b = 0.54")
plt.xlabel("Energy [KeV]")
plt.ylabel("FWHM")
# plt.ylim(0,3.2)
plt.show()

cols = ['FWHM',"energy","error"]
r = zip(fw, en, error)
with open('energy_resolution.csv', 'w') as f:
    write = csv.writer(f)

    write.writerow(cols)
    for row in r:
        w.writerow(row)

