import numpy as np
import pandas as pd
from statistics import mean
import matplotlib.pyplot as plt
import json
import os
from .foundation import *
import plotly.express as px
import sys

def PlotRawSpectrum(runs, spec='trapEmax', xhi=80000, xlo=0, yhi=30000, ylo=0, ysc = 'log', xsc = "linear", bin=8000, titl = 'Raw Spectrum', ytitl = 'counts', xtitl = 'Energy'):

    if isinstance(runs, int):
        t2_data = get_df(runs)
        counts, bins, bars = plt.hist(t2_data[spec], histtype='step', bins = bin)
        plt.yscale(ysc)
        plt.xscale(xsc)
        plt.ylim(yhi, ylo)
        plt.xlim(xlo,xhi)
        plt.title(titl)
        plt.xlabel(xtitl)
        plt.ylabel(ytitl)
        plt.show()
    else:
        t2_data = get_df_multiple(runs)
        counts, bins, bars = plt.hist(t2_data[spec], histtype='step', bins = bin)
        plt.yscale(ysc)
        plt.xscale(xsc)
        plt.ylim(yhi, ylo)
        plt.xlim(xlo,xhi)
        plt.title(titl)
        plt.xlabel(xtitl)
        plt.ylabel(ytitl)
        plt.show()


def PlotCalSpectrum(runs, spec='trapEmax', xhi=80000, xlo=0, yhi=30000, ylo=0, ysc = 'log', xsc = "linear", bin=8000, titl = 'Raw Spectrum', ytitl = 'counts', xtitl = 'Energy', det = "BeGe"):
    cwd = os.getcwd()
    file = cwd + '/detectors.json'
    with open(file, "r") as read_file:
        detectors = json.load(read_file)

    slope = detectors[det]['Calibration'][0]
    intercept = detectors[det]['Calibration'][1]

    if isinstance(runs, int):
        t2_data = get_df(runs)
        energyCal = [element * slope + intercept for element in t2_data[spec].nda]
        counts, bins, bars = plt.hist(energyCal, histtype='step', bins = bin)
        plt.yscale(ysc)
        plt.xscale(xsc)
        plt.ylim(yhi, ylo)
        plt.xlim(xlo,xhi)
        plt.title(titl)
        plt.xlabel(xtitl)
        plt.ylabel(ytitl)
        plt.show()
    else:
        t2_data = get_df_multiple(runs)
        energyCal = [element * slope + intercept for element in t2_data[spec].nda]
        counts, bins, bars = plt.hist(energyCal, histtype='step', bins = bin)
        plt.yscale(ysc)
        plt.xscale(xsc)
        plt.ylim(yhi, ylo)
        plt.xlim(xlo,xhi)
        plt.title(titl)
        plt.xlabel(xtitl)
        plt.ylabel(ytitl)
        plt.show()
