import numpy as np
import pandas as pd
from statistics import mean
import matplotlib.pyplot as plt
import json
import os
import foundation
import plotly.express as px


t1_data = foundation.get_t1_data(605)

df = t1_data["waveform"]["values"].nda[0]


plt.plot(df)
plt.show()
