import numpy as np
import pandas as pd
from statistics import mean
import matplotlib.pyplot as plt
import json
import os
import processes.foundation as fd
import plotly.express as px
import sys
import argparse

t1_data = fd.get_t1_data(1124)
print(t1_data["timestamp"].nda)
print(t1_data["channel"])
