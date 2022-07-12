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

arg('-i', '--index', nargs='*', type=int, help='index of waveform you want to see.')

args = par.parse_args()

runs = args.runs[0]
index = args.index[0]
try:
    dash = runs.index('-')
except:
    dash = None

if dash != None:
    start = runs[3:dash]
    end = runs[dash+4::]
    run_list = list(range(int(start),int(end)+1))
    t1_data = foundation.get_t1_data_multiple(run_list)

    df = t1_data[run_list[0]]["waveform"]["values"].nda[index]


else:
    t1_data = foundation.get_t1_data(runs[3::])

    df = t1_data["waveform"]["values"].nda[index]

plt.xlim(1000,2000)
plt.plot(df)
plt.show()
