import processes.foundation as fd
import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import argparse

"""
    This script was written by James Browning 8/22/22.
    This script is to print the table of any dsp data that is produced by pygama.
"""



def main():
    tables = fd.get_tables(1202)
    print(tables)

if __name__ == "__main__":
    main()
