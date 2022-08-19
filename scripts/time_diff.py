import processes.foundation as fd
import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import argparse

def main():

    run_lis = [1145]
    j = 0
    for run in run_lis:
        t2_data = fd.get_df(run, "Card1")
        for i in range(0, len(t2_data['timestamp'])):
            if t2_data['channel'].iloc[i] == 32:
                try:
                    first = t2_data['timestamp'].iloc[i-1]
                    next = t2_data['timestamp'].iloc[i+1]
                    tdiff = (next - first)*8
                    print(tdiff)
                    if tdiff > 33335000.0:
                        j += 1
                except:
                    print(i)

        #hol = t2_data['sus'].iloc[-1]
        print("j",j)
        first = t2_data['timestamp'].iloc[0]
        next = t2_data['timestamp'].iloc[-2]
        tdiff2 = (next - first)*8
        tdiff3 = tdiff2*(10**(-9))
        hz = len(t2_data['timestamp'])/tdiff3
        print(tdiff2)
        print(len(t2_data['timestamp']))
        print(hz)


if __name__ == "__main__":
    main()
