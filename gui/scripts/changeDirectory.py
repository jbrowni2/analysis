from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import filedialog
import sys
import json


def changeRawDirectory():
    data_folder = filedialog.askdirectory()
    with open('address.json', 'r') as read_file:
        data = json.load(read_file)

    data['tier1_dir'] = data_folder

    with open('address.json', 'w') as f:
        json.dump(data, f, indent=4)

def changeDaqDirectory():
    data_folder = filedialog.askdirectory()
    with open('address.json', 'r') as read_file:
        data = json.load(read_file)

    data['daq_dir'] = data_folder

    with open('address.json', 'w') as f:
        json.dump(data, f, indent=4)

def changeDspDirectory():
    data_folder = filedialog.askdirectory()
    with open('address.json', 'r') as read_file:
        data = json.load(read_file)

    data['tier2_dir'] = data_folder

    with open('address.json', 'w') as f:
        json.dump(data, f, indent=4)
