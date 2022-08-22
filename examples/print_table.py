import processes
import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import argparse

"""
    This script was written by James Browning 8/22/22.
    This script is to print the table of any dsp data that is produced by pygama.
"""



def main():
    doc = ""
    rthf = argparse.RawTextHelpFormatter
    par = argparse.ArgumentParser(description=doc, formatter_class=rthf)
    arg, st, sf = par.add_argument, 'store_true', 'store_false'

    arg('-r', '--runs', nargs=1, type=str,
            help="list of files to calibrate (-r 'Run####-Run####') ")
    arg('-t', '--table', nargs=1, type=str, help="name of table you wants to see (-t 'card1')")

    args = par.parse_args()

    runs = args.runs[0]
    tab = args.table[0]

    try:
        dash = runs.index('-')
    except:
        dash = None


    if dash != None:
        start = runs[3:dash]
        end = runs[dash+4::]
        run_list = list(range(int(start),int(end)+1))
        t2_data = get_df_multiple(run_list)
        print(t2_data)


    else:
        t2_data = processes.foundation.get_df(runs[3::], tab)


        print(t2_data)

if __name__ == "__main__":
    main()
