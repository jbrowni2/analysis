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

    runs = [1125]
    processes.show_spectrum.PlotCalSpectrum(runs, det = 'BeGe', tb = 'Card1', xhi=1000, xlo=0, yhi=3000, ylo=0, bin=3000)


if __name__ == "__main__":
    main()
