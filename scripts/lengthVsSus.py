import processes
import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import argparse

def main():

    run_lis = [960, 961, 963, 964, 965, 966, 967, 968]
    Length = [5000, ]
    sus = []
    for run in run_lis:
        t2_data = processes.foundation.get_df(run)
        hol = t2_data['sus'].iloc[-1]/(len(t2_data['sus'])+t2_data['sus'].iloc[-1])
        sus.append(hol)
        hold = (len(t2_data['sus'])+t2_data['sus'].iloc[-1])/60
        hz.append(hold)

    plt.scatter(hz, sus)
    plt.xlabel('events per second')
    plt.ylabel('Percent of Events with Multiple Lengths')
    plt.title('Plot of data throwouts as a function of trigger rate')
    plt.show()


if __name__ == "__main__":
    main()
