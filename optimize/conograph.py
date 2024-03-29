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




def peak_width(tb, verbosity, make_plot=False):

    m = 0.040862505104599725
    b = -0.1689243143849808
    calib = m*tb['trapEmax'].nda + b

    binning = np.linspace(30,70,num=3000)
    
    energy = copy.deepcopy(calib)
    #counts, bins, bars = plt.hist(energy, histtype='step', bins=100000)
    counts, bins = np.histogram(energy,bins=binning)

    lower = hA.find_nearest_bin(bins,30)
    upper = hA.find_nearest_bin(bins,70)
    ydata = counts[lower:upper]
    xdata = bins[lower:upper]

    gmodel = Model(fM.linDubGaus)
    i = np.argmax(ydata)
    #params = gmodel.make_params(A=700, m1=315.5, s1=0.5, H_tail=-0.000001, H_step=1, tau=-0.5, slope=-6, intrcpt=180)
    params = gmodel.make_params(a1=400, m1=xdata[i], s1=0.07, a2=400, m2=xdata[i]+0.1, s2=0.07, slope=-0.046, intrcpt=58)
    #params['s1'].vary = False
    result = gmodel.fit(ydata,params, x=xdata)

    sigma1 = result.params['s1'].value
    fw1 = 2.355*sigma1
    err = result.params['s1'].stderr
    err1 = err*2.355
    sigma2 = result.params['s2'].value
    fw2 = 2.355*sigma2
    err = result.params['s2'].stderr
    err2 = err*2.355
    energy = result.params['m1'].value

    print(fw1)
    print(fw2)
    #sigma = result.params['s1'].value
    #fw = 2.355*sigma
    #energy = result.params['m1'].value

    
    
    
    """
    print(result.fit_report())
    plt.hist(calib, histtype='step', bins=binning)
    plt.xlim(45, 46)
    #plt.ylim(0,00)
    plt.xlabel("Energy [keV]")
    plt.plot(xdata, result.best_fit, 'r-', label='best fit')
    plt.title("Fit of 1725 Pulser FWHM")
    plt.show()

    print(fw1)
    print(fw2)
    inputfw = input("fw1 or fw2")
    if inputfw == "fw1":
        print("hello")
        return fw1, err1
    if inputfw == "fw2":
        return fw2, err2
    """

    return fw1, err1






def main():
    conf_file = "downSampleTest.json"
    with open(conf_file) as f:
        dsp_config = json.load(f, object_pairs_hook=OrderedDict)
        
    cwd = os.getcwd()
    file = cwd + '/address.json'
    with open(file, 'r') as read_file:
        data = json.load(read_file)

    file = data["tier1_dir"] + "/opt"
    optSto = LH5Store(file)
    tb_wfs, nwfs = optSto.read_object('Card1/',"Run18.lh5")

    rise_arr = np.linspace(3,20,18)
    flat_arr = np.linspace(0.9,0.9,1)

    zz = np.zeros(len(rise_arr)*len(flat_arr))
    err = np.zeros(len(rise_arr)*len(flat_arr))

   # rises = np.ones(len(zz))*10
    

    

    for i,flat in enumerate(flat_arr):
        for j,rise in enumerate(rise_arr):
            print(j)
            flat_units = str(flat)+'*us'
            rise_units = str(rise)+'*us'
            args = ['sub1',rise_units,flat_units,'wf_trap']
            dsp_config['processors']['wf_trap']['args'] = args

            fom = run_one_dsp(tb_wfs, dsp_config,fom_function=peak_width, verbosity=True)
            #fom = run_one_dsp(tb_wfs, dsp_config, verbosity=True)
            #peak_width(fom, 1, True)

            zz[i+j], err[i+j] = fom

    df = pd.DataFrame({"FWHM": zz, "rise": rise_arr, "flat": flat_arr, "error": err})
    df.to_csv("RiseNoiseChange.csv")







if __name__ == "__main__":
    main()