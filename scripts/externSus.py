import processes
import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import argparse

def main():

    run_lis = [1018, 1019, 1020, 1021, 1022, 1023, 1024, 1025, 1026, 1027, 1028, 1029]
    Length = [5000, 10000, 15000, 54464, 25000, 30000, 35000, 40000, 45000, 50000, 20000, 60000]
    sus = []
    t2_data = processes.foundation.get_df(run)
    hol = t2_data['sus'].iloc[-1]/(len(t2_data['sus'])+t2_data['sus'].iloc[-1])


if __name__ == "__main__":
    main()
