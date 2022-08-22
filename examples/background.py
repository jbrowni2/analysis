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

    processes.show_spectrum.PlotRawSpectrum(1035, 'Card1', xhi=400000, xlo=50000, yhi=1000, ylo=10, bin=80000)


if __name__ == "__main__":
    main()
