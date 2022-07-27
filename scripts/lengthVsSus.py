import processes
import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import argparse

def main():

    run_lis = [1043, 1044, 1045, 1046, 1047, 1067]
    poll = [10000, 5000, 2000, 1000, 100, 20000]
    sus = []
    for run in run_lis:
        t2_data = processes.foundation.get_df(run)
        hol = t2_data['sus'].iloc[-1]/(len(t2_data['sus'])+t2_data['sus'].iloc[-1])
        #hol = t2_data['sus'].iloc[-1]
        sus.append(hol)

    plt.scatter(poll, sus)
    plt.xlabel('Polling rate of Events')
    plt.ylabel('Percent of Events with different Polling rate')
    plt.title('Plot of data throwouts as a function of polling rates')
    plt.show()


if __name__ == "__main__":
    main()
