import os
import json
import matplotlib.pyplot as plt
from statistics import mean
import pandas as pd
import numpy as np
import os
from scipy import stats, special
import matplotlib.colors as mcolors
from math import exp, sqrt, pi, erfc
from lmfit import Model
from scipy.optimize import curve_fit
from pygama import lh5
from pygama import __version__ as pygama_version
from pygama.dsp.ProcessingChain import ProcessingChain
from pygama.dsp.units import *
from pygama import lh5
from pygama.utils import update_progress
import pygama.git as git
from pygama.dsp.build_processing_chain import *
from scipy.fft import fft, ifft, fftfreq


def find_nearest_bin(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx


def get_t2_data(run):

    with open('coherent.json', 'r') as read_file:
        data = json.load(read_file)
    # datadir = os.getenv(data[])
    #ncsu_data_dir = datadir + "/research"
    #t1_dir = os.getenv(data['tier1_dir'])
    t2_dir = data['tier2_dir']
    f_raw = t2_dir + '/Run' + str(run)
    raw_store = lh5.Store()
    lh5_file = raw_store.gimme_file(f_raw, 'r')

    lh5_tables = []
    lh5_keys = raw_store.ls(f_raw)

    for tb in lh5_keys:
        if "dsp" not in tb:
            tbname = raw_store.ls(lh5_file[tb])[0]
        if "dsp" in tbname:
            tb = tb + '/' + tbname  # g024 + /dsp
        lh5_tables.append(tb)

    lh5_tables.pop(-1)

    buffer_len = 10000000000000000
    for tb in lh5_tables:
        # load primary table and build processing chain and output table
        tot_n_rows = raw_store.read_n_rows(tb, f_raw)

        chan_name = tb.split('/')[0]
        # db_dict = database.get(chan_name) if database else None
        t2_noise, n_rows_read = raw_store.read_object(tb, f_raw, start_row=0, n_rows=buffer_len)

        return t2_noise


def get_t1_data(run):

    with open('coherent.json', 'r') as read_file:
        data = json.load(read_file)

    # datadir = os.getenv(data[])
    #ncsu_data_dir = datadir + "/research"
    #t1_dir = data['tier1_dir']
    #t1_dir = os.getenv("data/tier1")



    datadir = os.getenv("HOME")
    ncsu_data_dir = datadir + "/data"
    t1_dir = ncsu_data_dir + "/tier1"


    f_raw = t1_dir + '/Run' + str(run)
    raw_store = lh5.Store()
    lh5_file = raw_store.gimme_file(f_raw, 'r')

    lh5_tables = []
    lh5_keys = raw_store.ls(f_raw)

    for tb in lh5_keys:
        if "raw" not in tb:
            tbname = raw_store.ls(lh5_file[tb])[0]
        if "raw" in tbname:
            tb = tb + '/' + tbname  # g024 + /dsp
        lh5_tables.append(tb)

    # lh5_tables.pop(-1)

    buffer_len = 10000000000000000
    for tb in lh5_tables:
        # load primary table and build processing chain and output table
        tot_n_rows = raw_store.read_n_rows(tb, f_raw)

        chan_name = tb.split('/')[0]
        # db_dict = database.get(chan_name) if database else None
        t1_noise, n_rows_read = raw_store.read_object(tb, f_raw, start_row=0, n_rows=buffer_len)


    return t1_noise


def get_t2_data_multiple(runs):
    with open('coherent.json', 'r') as read_file:
        data = json.load(read_file)
    # datadir = os.getenv(data[])
    #ncsu_data_dir = datadir + "/research"
    #t1_dir = os.geten(data['tier1_dir'])
    t2_dir = data['tier2_dir']
    f_raw = t2_dir + '/Run' + str(runs[0])
    raw_store = lh5.Store()
    lh5_file = raw_store.gimme_file(f_raw, 'r')

    lh5_tables = []
    lh5_keys = raw_store.ls(f_raw)

    for tb in lh5_keys:
        if "dsp" not in tb:
            tbname = raw_store.ls(lh5_file[tb])[0]
        if "dsp" in tbname:
            tb = tb + '/' + tbname  # g024 + /dsp
        lh5_tables.append(tb)

    lh5_tables.pop(-1)

    buffer_len = 10000000000000000
    for tb in lh5_tables:
        # load primary table and build processing chain and output table
        tot_n_rows = raw_store.read_n_rows(tb, f_raw)

        chan_name = tb.split('/')[0]
        # db_dict = database.get(chan_name) if database else None
        t2_noise, n_rows_read = raw_store.read_object(
            tb, f_raw, start_row=0, n_rows=buffer_len)

    for run in runs:
        f_raw = t2_dir + '/Run' + str(run)
        raw_store = lh5.Store()
        lh5_file = raw_store.gimme_file(f_raw, 'r')

        lh5_tables = []
        lh5_keys = raw_store.ls(f_raw)

        for tb in lh5_keys:
            if "dsp" not in tb:
                tbname = raw_store.ls(lh5_file[tb])[0]
            if "dsp" in tbname:
                tb = tb + '/' + tbname  # g024 + /dsp
            lh5_tables.append(tb)

        lh5_tables.pop(-1)

        buffer_len = 10000000000000000
        for tb in lh5_tables:
            # load primary table and build processing chain and output table
            tot_n_rows = raw_store.read_n_rows(tb, f_raw)

            chan_name = tb.split('/')[0]
            # db_dict = database.get(chan_name) if database else None
            t2_noise[run], n_rows_read = raw_store.read_object(
                tb, f_raw, start_row=0, n_rows=buffer_len)

    return t2_noise


def get_t1_data_multiple(runs):
    with open('coherent.json', 'r') as read_file:
        data = read_file
    # datadir = os.getenv(data[])
    #ncsu_data_dir = datadir + "/research"
    #t1_dir = os.getenv(data['tier1_dir'])
    t1_dir = os.getenv(data['tier1_dir'])

    f_raw = t1_dir + '/Run' + str(runs[0])
    raw_store = lh5.Store()
    lh5_file = raw_store.gimme_file(f_raw, 'r')

    lh5_tables = []
    lh5_keys = raw_store.ls(f_raw)

    for tb in lh5_keys:
        if "raw" not in tb:
            tbname = raw_store.ls(lh5_file[tb])[0]
        if "raw" in tbname:
            tb = tb + '/' + tbname  # g024 + /dsp
        lh5_tables.append(tb)

    # lh5_tables.pop(-1)

    buffer_len = 10000000000000000
    for tb in lh5_tables:
        # load primary table and build processing chain and output table
        tot_n_rows = raw_store.read_n_rows(tb, f_raw)

        chan_name = tb.split('/')[0]
        # db_dict = database.get(chan_name) if database else None
        t2_noise, n_rows_read = raw_store.read_object(
            tb, f_raw, start_row=0, n_rows=buffer_len)

    for run in runs:
        f_raw = t1_dir + '/Run' + str(run)
        raw_store = lh5.Store()
        lh5_file = raw_store.gimme_file(f_raw, 'r')

        lh5_tables = []
        lh5_keys = raw_store.ls(f_raw)

        for tb in lh5_keys:
            if "raw" not in tb:
                tbname = raw_store.ls(lh5_file[tb])[0]
            if "raw" in tbname:
                tb = tb + '/' + tbname  # g024 + /dsp
            lh5_tables.append(tb)

        # lh5_tables.pop(-1)

        buffer_len = 10000000000000000
        for tb in lh5_tables:
            # load primary table and build processing chain and output table
            tot_n_rows = raw_store.read_n_rows(tb, f_raw)

            chan_name = tb.split('/')[0]
            # db_dict = database.get(chan_name) if database else None
            t1_noise[run], n_rows_read = raw_store.read_object(
                tb, f_raw, start_row=0, n_rows=buffer_len)

    return t1_noise


def get_peak(data, min, max):
    counts, bins, bars = plt.hist(data, histtype='step', bins=160000)

    peak_min, peak_max = min, max

    peak_range = find_nearest_bin(bins, peak_min), find_nearest_bin(bins, peak_max)

    peak_idx = np.argmax(counts[peak_range[0]:peak_range[1]]) + peak_range[0]

    peak = bins[peak_idx]

    return peak


def lingaus(x, a1, m1, s1, slope, intrcpt):
    """1-d gaussian with linear background: gaussian(x, amp, cen, wid)"""
    return a1 * np.exp(-(x-m1)**2 / (2*s1**2)) + slope*x + intrcpt


def noise(x, h1, h2, h3):
    fit = h1*x + h2/x + h3
    return fit


def res(x, m, c, intrcpt):
    fit = m*np.power(x + c*(np.power(x, 2)), 0.5) + intrcpt
    return fit


def get_df(run):
    data = get_t2_data(run)
    dictionary = dict()
    for col in data:
        dictionary[col] = data[col].nda
        #d = {'channel': data['channel'].nda, 'trapEmax': data['trapEmax'].nda,
        #    'timestamp': data['timestamp'].nda}
    #print(dictionary)
    df = pd.DataFrame(data=dictionary)
    return df

def get_df_multiple(runs):
    #data = get_t2_data_multiple(runs)
    lis = []
    for run in runs:
        df = get_df(run)
        lis.append(df)

    dictionary = pd.concat(lis)
    dictionary = dictionary.reset_index(drop=True)
    return dictionary



def get_fwhm(data, min, max, peak):
    counts, bins, bars = plt.hist(data, histtype='step', bins=160000)
    plt.xlim(min, max)
    plt.ylim(0, 150)
    lower = find_nearest_bin(bins, min)
    upper = find_nearest_bin(bins, max)
    ydata = counts[lower:upper]
    xdata = bins[lower:upper]

    gmodel = Model(lingaus)
    # params = gmodel.make_params(A=700, m1=315.5, s1=0.5, H_tail=-0.000001, H_step=1, tau=-0.5, slope=-6, intrcpt=180)
    params = gmodel.make_params(a1=600, m1=peak, s1=0.1, slope=-0.046, intrcpt=58)
    # params['s1'].vary = False
    result = gmodel.fit(ydata, params, x=xdata)

    sigma = result.params['s1'].value
    FWHM = 2.355*sigma
    err = 2.355*result.params['s1'].stderr
    energy = result.params['m1'].value

    return FWHM, err, energy


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
