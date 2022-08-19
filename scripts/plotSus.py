import numpy as np
import pandas as pd
from statistics import mean
import matplotlib.pyplot as plt
import json
import os
import processes.foundation as fd
import plotly.express as px
import sys


def main():

    runs = [1124,1125,1126,1127]
    data = fd.get_df_multiple(runs, 'Card1')
    lis = []

    for i in range(0, len(data['trapEmax'])):
        if data['channel'].iloc[i]==33:
            lis.append(data['trapEmax'].iloc[i])

    plt.hist(lis, histtype='step', bins = 30000)
    plt.title("Plot Of Values From 2nd Event in Double Length")
    plt.xlabel("Energy [keV]")
    plt.ylabel("Counts")
    plt.xlim(0,1000)
    plt.show()


if __name__ == "__main__":
    main()
