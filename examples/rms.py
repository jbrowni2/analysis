import numpy as np
import pandas as pd
from statistics import mean
import matplotlib.pyplot as plt
import json
import os
import processes.foundation as fd
import processes.fitModel as fM
import processes.histogramAction as hA
import plotly.express as px
import sys
import argparse


def main():

    t1_data = fd.get_t1_data(1205)

    rms = hA.findRms(t1_data[0]["waveform"]["values"].nda[0])
    print(rms)

if __name__ == "__main__":
    main()
