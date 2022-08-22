import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from scipy import stats
from math import exp
import processes.foundation as fd
import processes.fitModel as fM
import processes.histogramAction as hA
from math import exp, sqrt, pi, erfc
from lmfit import Model


def main():


    fw = []
    energy = []
    yerr = []

    runs_list = [[1119,1120,1121,1122], [1124,1125,1126,1127], [1128,1129,1130]]
    energy_list = [[1172, 1333], [80, 270, 310, 360, 390], [660]]
    upLow = [[[1072, 1272], [1233, 1433]], [[50, 120], [260, 280], [290, 330], [340, 370], [370, 420]], [[620, 700]]]
    i = 0
    for runs in runs_list:
        t2_data = fd.get_df_multiple(runs, 'Card1')

        counts, bins, bars = plt.hist(t2_data['trapEmax'], histtype='step', bins=160000)
        j = 0
        for ran in upLow[i]:
            lower = hA.find_nearest_bin(bins,ran[0])
            upper = hA.find_nearest_bin(bins,ran[1])
            ydata = counts[lower:upper]
            xdata = bins[lower:upper]

            gmodel = Model(fM.lingaus)
            #params = gmodel.make_params(A=700, m1=315.5, s1=0.5, H_tail=-0.000001, H_step=1, tau=-0.5, slope=-6, intrcpt=180)
            params = gmodel.make_params(a1=1000, m1=energy_list[i][j], s1=2.0, slope=-0.046, intrcpt=58)
            #params['s1'].vary = False
            result = gmodel.fit(ydata,params, x=xdata)

            sigma = result.params['s1'].value
            fw.append(2.355*sigma)
            yerr.append(2.355*result.params['s1'].stderr)
            energy.append(result.params['m1'].value)

            j += 1



        i += 1

    print(fw)
    print(energy)

    #This code fits the resolution map to the equation it should follow.
    gmodel = Model(fM.res)
    #params = gmodel.make_params(A=200, m1=277, s1=0.9, H_tail=-1, H_step=-1, tau=-1, slope=-0.12, intrcpt=180)
    params = gmodel.make_params(m=0.02,intrcpt = 6.0, c = 0.5)
    #params['intrcpt'].vary = False
    #params['m'].vary = False
    #params['c'].vary = False
    result = gmodel.fit(fw,params, x=energy)



    m = result.params['m'].value
    c = result.params['c'].value
    intrcpt = result.params['intrcpt'].value
    x = np.arange(0,1500,0.1)
    y = m*np.power(x + c*(np.power(x,2)),0.5) + intrcpt

    plt.figure().clear()

    plt.errorbar(energy,fw,yerr=yerr, fmt='o')
    plt.plot(x,y)
    plt.title("Energy Resolution of Detector 1725")
    plt.text(0,3.0, "Function is m*(E + c*(E^2)) + b")
    #plt.text(1000,2.0,"m = 0.003")
    #plt.text(1000,1.8,"c = 0.326")
    #plt.text(1000,1.6,"b = 0.54")
    plt.xlabel("Energy [KeV]")
    plt.ylabel("FWHM")
    #plt.ylim(0,3.2)
    plt.show()

    print('m',m)
    print('c',c)
    print('intrcpt', intrcpt)



if __name__ == "__main__":
    main()















"""
runs = [1128,1129,1130]
t2_data = fd.get_df_multiple(runs, 'Card1')


counts, bins, bars = plt.hist(t2_data['trapEmax'], histtype='step', bins=160000)
lower = fd.find_nearest_bin(bins,620)
upper = fd.find_nearest_bin(bins,700)
ydata = counts[lower:upper]
xdata = bins[lower:upper]



gmodel = Model(fd.lingaus)
#params = gmodel.make_params(A=700, m1=315.5, s1=0.5, H_tail=-0.000001, H_step=1, tau=-0.5, slope=-6, intrcpt=180)
params = gmodel.make_params(a1=1000, m1=660, s1=2.0, slope=-0.046, intrcpt=58)
#params['s1'].vary = False
result = gmodel.fit(ydata,params, x=xdata)

print(result.fit_report())
plt.hist(t2_data['trapEmax'], histtype='step', bins=160000)
plt.xlim(620, 700)
plt.ylim(0,1000)
plt.xlabel("Energy [keV]")
#plt.text(76.5,1000, "FWHM = 0.459(4) keV")
plt.plot(xdata, result.best_fit, 'r-', label='best fit')
plt.title("Fit of Noise from Ge Detector")
plt.show()

sigma = result.params['s1'].value
FWHM = 2.355*sigma
err2 = 2.355*result.params['s1'].stderr



fw = [FWHM]
energy = [result.params['m1'].value]
yerr = [err2]
"""
