import foundation
import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import argparse
import seaborn as sns

def main():
    doc = ""
    rthf = argparse.RawTextHelpFormatter
    par = argparse.ArgumentParser(description=doc, formatter_class=rthf)
    arg, st, sf = par.add_argument, 'store_true', 'store_false'

    arg('-r', '--runs', nargs=1, type=str,
            help="list of files to calibrate (-r 'Run####-Run####') ")

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
        sns.pairplot(t2_data)
        plt.show()

        #print(t2_data[int(start)])


    else:
        t2_data = foundation.get_df(runs[3::])
        plot = sns.pairplot(t2_data)
        plot.figure.savefig("pairplot.png")
        #for col in t2_data:
        #    print(col)



if __name__ == "__main__":
    main()
