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


def lingaus(x, a1, m1, s1, slope, intrcpt):
    """1-d gaussian with linear background: gaussian(x, amp, cen, wid)"""
    return a1 * np.exp(-(x-m1)**2 / (2*s1**2)) + slope*x + intrcpt

def linDubGaus(x, a1, m1, s1, a2, m2, s2, slope, intrcpt):
    """1-d gaussian with linear background: gaussian(x, amp, cen, wid)"""
    return a1 * np.exp(-(x-m1)**2 / (2*s1**2)) + slope*x + intrcpt + a2 * np.exp(-(x-m2)**2 / (2*s2**2))


def noise(x, h1, h2, h3):
    fit = h1*x + h2/x + h3
    return fit


def energyResolution(x, m, c, intrcpt):
    fit = m*np.power(x + c*(np.power(x, 2)), 0.5) + intrcpt
    return fit


def noise_fit(rise, flat, fw, error):
    # This code fits the resolution map to the equation it should follow.
    gmodel = Model(noise)
    #params = gmodel.make_params(A=200, m1=277, s1=0.9, H_tail=-1, H_step=-1, tau=-1, slope=-0.12, intrcpt=180)
    params = gmodel.make_params(h1=0.005, h2=1.2, h3=0.5)
    #params['h2'].vary = False
    #params['m'].vary = False
    result = gmodel.fit(fw, params, x=rise)
    return result.params['h1'].value, result.params['h2'].value, result.params['h3'].value, result


def energy_fit(fw, energy, error):
    gmodel = Model(res)
    arams = gmodel.make_params(m=0.04915, intrcpt=0.5, c=0.3)
    result = gmodel.fit(fw, params, x=energy)
