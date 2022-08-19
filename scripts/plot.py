import numpy as np
import pandas as pd
from statistics import mean
import matplotlib.pyplot as plt
import json
import os
import processes
import plotly.express as px
import sys

def main():

    runs = [1124,1125,1126,1127]
    processes.show_spectrum.PlotRawSpectrum(runs, 'Card1', xhi=1000, xlo=0, yhi=1000, ylo=10, bin=160000, ysc='linear')


if __name__ == "__main__":
    main()
