import numpy as np
import pandas as pd
from statistics import mean
import matplotlib.pyplot as plt
import json
import os
import processes as pr
import plotly.express as px
import sys
import argparse


def main():

    t1_data = pr.foundation.get_t1_data(1205, "Card1")
    dat=t1_data[0]["waveform"]["values"].nda[0]


    df = pd.DataFrame(dat).T

    print(df)


if __name__ == "__main__":
    main()
