import numpy as np
import pandas as pd
from statistics import mean
import matplotlib.pyplot as plt
import json
import os
import foundation
import plotly.express as px
import sys
import argparse

doc = ""
rthf = argparse.RawTextHelpFormatter
par = argparse.ArgumentParser(description=doc, formatter_class=rthf)
arg, st, sf = par.add_argument, 'store_true', 'store_false'

arg('-r', '--runs', nargs=1, type=str,
        help="list of files to calibrate (-r 'Run####-Run####') ")

arg('-b', '--bin', nargs='*', type=int, help='bins number for histogram')
arg('-x', '--xlim', nargs= 2, type=int, help='lower and upper limits in x plane (-x #### ####)')

args = par.parse_args()

runs = args.runs[0]
try:
    dash = runs.index('-')
except:
    dash = None

if dash != None:
    start = runs[3:dash]
    end = runs[dash+4::]
    run_list = list(range(int(start),int(end)+1))
    t2_data = foundation.get_df_multiple(run_list)
    try:
        bines = args.bin[0]
    except:
        bines = 16000
    counts, bins, bars = plt.hist(t2_data['trapEmax'], histtype='step', bins = bines)
    plt.yscale('log')
    plt.xlim(args.xlim[0],args.xlim[1])
    plt.show()



else:
    #print(runs[3::])
    t2_data = foundation.get_df(runs[3::])


    try:
        bines = args.bin[0]
    except:
        bines = 16000
    counts, bins, bars = plt.hist(t2_data['trapEmax'], histtype='step', bins=bines)
    plt.yscale('log')
    plt.xlim(args.xlim[0],args.xlim[1])
    plt.show()
