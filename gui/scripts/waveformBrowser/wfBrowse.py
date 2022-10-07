from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import filedialog
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
import processes.foundation as fd
import processes.fitModel as fM
import processes.histogramAction as hA
import os
from tkinter import messagebox
from tkinter import filedialog
import json
import customtkinter

from wfNorm import norm
from wfTrapFilter import trapFiltered
from wfWavelet import waveletFiltered
from wfFFt import fourierFiltered



def test():
    pass

def browseClass(master):
    global wfBrowserWindow
    wfBrowserWindow = customtkinter.CTkToplevel()
    wfBrowserWindow.configure(bg='gray20')

    # sets the title of the
    # Toplevel widget
    wfBrowserWindow.title("Wf Browser Window")

    # sets the geometry of toplevel
    wfBrowserWindow.geometry("1400x800")

    my_menu = Menu(wfBrowserWindow)
    wfBrowserWindow.config(menu=my_menu)


    #create a menu item

    file_menu = Menu(my_menu)
    my_menu.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="exit", command=master.quit)

    action_menu = Menu(my_menu)
    my_menu.add_cascade(label="browse", menu=action_menu)
    action_menu.add_command(label="Waveform", command=lambda: norm(wfBrowserWindow))
    action_menu.add_command(label="Trap Filter", command=lambda: trapFiltered(wfBrowserWindow))
    action_menu.add_command(label="Fourier Transform", command=lambda: fourierFiltered(wfBrowserWindow))
    action_menu.add_command(label="Wavelet Transform", command=lambda: waveletFiltered(wfBrowserWindow))
