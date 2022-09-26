"""
This filter was written by James B.
This script was written to fit noise data.
"""

import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import h5py 
import json
import copy
from collections import OrderedDict
from lmfit import Model
import os

from pygama.pargen.dsp_optimize import run_one_dsp
from pygama.pargen.dsp_optimize import run_grid
from pygama.pargen.dsp_optimize import ParGrid
from pygama.lgdo.lh5_store import LH5Store
import pygama.math.histogram as pgh
import pygama.math.peak_fitting as pgf


sys.path.insert(1, '../analysis/')
import processes.foundation as fd
import processes.fitModel as fM
import processes.histogramAction as hA


def main():
    df = pd.read_csv('FlatNoiseChange.csv')

    df["FW2"] = df["FWHM"]**2
    #df["rise"] = np.linspace(3,20,18)
    df["err2"] = df["FW2"]*(df["error"]/df["FWHM"])
    print(df)

    gmodel = Model(fM.noise)
    params = gmodel.make_params(h1=0.1, h2=0.1, h3=0)
    #params["h3"].vary = False
    result = gmodel.fit(df["FW2"].values,params, x=df["flat"].values)

    print(result.fit_report())

    h1 = result.params['h1'].value
    h2 = result.params["h2"].value
    h3 = result.params["h3"].value

    x = np.linspace(0.1,2.0,1000)
    y = fM.noise(x, h1, h2, h3)
    y1 = h1*x
    y2 = h2/x
    y3 = np.ones(len(x))*h3
    print(y3)

    plt.errorbar(df["flat"], df["FW2"], yerr=df["err2"], fmt='bo')
    plt.plot(x,y, '-r', label="Fit")
    plt.plot(x, y1, 'g--', label="Parrallel")
    plt.plot(x, y2, 'b--', label="Series")
    plt.plot(x, y3, 'y', label="White Noise")
    plt.legend()
    plt.xlabel("Rise [us]")
    plt.ylabel("FWHM^2 [keV^2]")
    plt.title("FWHM^2 of Pulsar Peak as a Function of Rise Time")
    #plt.text(10, 0.08,"Fit = h1*x + h2/x + h3")
    #plt.text(10, 0.075, "h1 = 0.00179(8)")
    #plt.text(10, 0.07, "h2 = 0.169(6)")
    #plt.text(10, 0.065, "h3 = -0.0097(16)")
    plt.show()



if __name__ == "__main__":
    main()