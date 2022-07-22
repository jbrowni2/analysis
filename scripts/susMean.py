import processes
import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import argparse

def main():
    t2_data = processes.foundation.get_df(1032, 'Card1')
    sus = 0
    for i in range(1,1640):
        hol = t2_data['sus'].iloc[i]-t2_data['sus'].iloc[i-1]
        sus = sus + hol

    susAverage = sus/1640

    print(susAverage)


if __name__ == "__main__":
    main()
