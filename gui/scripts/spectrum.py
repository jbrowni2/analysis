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
import os
from tkinter import messagebox
from tkinter import filedialog
import json


class spectrumViewer:

    def pick_file(self, e):

        file = self.runFile.get()
        tables = fd.get_tables(int(file[3:7]))
        self.run_table.config(values=tables)
        self.run_table.current(0)


    def graph(self, fileName, table, bin):
        self.fig = Figure(figsize = (5,5) , dpi = 100)
        df = fd.get_df(str(fileName[3:7]), table)

        plot1 = self.fig.add_subplot(111)
        plot1.hist(df['trapEmax'], histtype='step', bins=bin)

        self.canvas = Canvas(self.spectrumViewerWindow, width=700, height=594)
        self.canvas.grid(row=0, column=100)

        self.figure_canvas = FigureCanvasTkAgg(self.fig, self.spectrumViewerWindow)
        self.figure_canvas.draw()
        self.figure_canvas.get_tk_widget().grid(row=0,column=10,rowspan=7,padx=5,pady=2)

        self.toolbar_frame = Frame(self.canvas)
        self.toolbar = NavigationToolbar2Tk(self.figure_canvas, self.toolbar_frame)
        self.toolbar.update()
        self.toolbar_frame.grid(row=9, column=10, pady=2)

    def __init__(self, master):

        self.spectrumViewerWindow = Tk()

        # sets the title of the
        # Toplevel widget
        self.spectrumViewerWindow.title("Energy Spectrum Window")

        # sets the geometry of toplevel
        self.spectrumViewerWindow.geometry("1400x600")

        options = os.listdir("/home/jlb1694/data/raw")

        self.runFile = ttk.Combobox(self.spectrumViewerWindow, values=options)
        self.runFile.current(0)
        self.runFile.grid(row=2, column=0)
        #bindthecombobox
        self.runFile.bind("<<ComboboxSelected>>", self.pick_file)

        self.run_table = ttk.Combobox(self.spectrumViewerWindow, value=[" "])
        self.run_table.grid(row=4, column=0)

        self.bin = Entry(self.spectrumViewerWindow, width=35, borderwidth=5)
        self.bin.grid(row=6, column=0, padx=10, pady=10)

        self.my_button = Button(self.spectrumViewerWindow, text = "Graph It!", command=lambda: self.graph(self.runFile.get(), str(self.run_table.get()), int(self.bin.get()))).grid(row=0, column=0)
        self.mylbl = Label(self.spectrumViewerWindow, text = "What run number would you like to browse?").grid(row=1, column=0)
        self.mylbl2 = Label(self.spectrumViewerWindow, text = "What table would you like to browse?").grid(row=3, column=0)
        self.mylbl3 = Label(self.spectrumViewerWindow, text = "What Binning would you like?").grid(row=5, column=0)
