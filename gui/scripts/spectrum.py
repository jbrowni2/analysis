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

    def clear(self):
        for widget in self.spectrumViewerWindow.winfo_children():
            widget.destroy()

    def fit(self):
        pass

    def createEntries(self, numPeak):
        self.peakMinEntries = []
        self.peakMaxEntries = []
        self.peak_min.delete(0, END)
        self.peak_max.delete(0, END)
        if numPeak != 0:
            for i in range(int(numPeak)):
                self.peak_min = Entry(self.spectrumViewerWindow)
                self.peak_min.grid(row=i+2, column=15, pady=20, padx=5)
                self.peakMinEntries.append(self.peak_min)
            for i in range(int(numPeak)):
                self.peak_max = Entry(self.spectrumViewerWindow)
                self.peak_max.grid(row=i+2, column=16, pady=20, padx=5)
                self.peakMaxEntries.append(self.peak_max)

    def set_calibrate(self):
        peakMinEntries = []
        my_entries = []
        self.num_range = Entry(self.spectrumViewerWindow, width=35, borderwidth=5)
        self.num_range.grid(row=1, column=15, padx=10, pady=10)
        self.myRangeLabel = Label(self.spectrumViewerWindow, text = "How many peaks are you fitting?").grid(row=0, column=15)
        self.num_range.insert(0, '0')

        self.add_entries = Button(self.spectrumViewerWindow, text = "Add Entries!", command=lambda: self.createEntries(int(self.num_range.get()))).grid(row=0, column=16)




    def pick_file(self, e):

        file = self.runFileStart.get()
        tables = fd.get_tables(int(file[3:7]))
        self.run_table.config(values=tables)
        self.run_table.current(0)

    def Multi_File(self):
        self.clear()

        with open('address.json', 'r') as read_file:
            data = json.load(read_file)

        options = os.listdir(data["tier2_dir"])

        self.runFileStart = ttk.Combobox(self.dataFrame, values=options)
        self.runFileStart.current(0)
        self.runFileStart.grid(row=2, column=0)
        #bindthecombobox
        self.runFileStart.bind("<<ComboboxSelected>>", self.pick_file)

        self.runFileEnd = ttk.Combobox(self.dataFrame, values=options)
        self.runFileEnd.current(0)
        self.runFileEnd.grid(row=4, column=0)


        self.run_table = ttk.Combobox(self.dataFrame, value=[" "])
        self.run_table.grid(row=6, column=0)

        self.bin = Entry(self.dataFrame, width=35, borderwidth=5)
        self.bin.grid(row=8, column=0, padx=10, pady=10)

        self.my_button = Button(self.dataFrame, text = "Graph It!", command=lambda: self.graphMultiple(self.runFileStart.get(), self.runFileEnd.get(), str(self.run_table.get()), int(self.bin.get()))).grid(row=0, column=0)
        self.mylbl = Label(self.dataFrame, text = "What run number would you like to Start with?").grid(row=1, column=0)
        self.mylbl4 = Label(self.dataFrame, text = "What run number would you like to End with?").grid(row=3, column=0)
        self.mylbl2 = Label(self.dataFrame, text = "What table would you like to plot?").grid(row=5, column=0)
        self.mylbl3 = Label(self.dataFrame, text = "What Binning would you like?").grid(row=7, column=0)

        #creating the Menu

        #my_menu = Menu(self.spectrumViewerWindow)
        #self.spectrumViewerWindow.config(menu=my_menu)


        #create a menu item

        #file_menu = Menu(my_menu)
        #my_menu.add_cascade(label="File", menu=file_menu)
        #file_menu.add_command(label="Use Multiple File", command=self.Multi_File)
        #file_menu.add_separator()
        #file_menu.add_command(label="Use Single File", command=self.Single_File)

    def Single_File(self):
        self.clear()


        with open('address.json', 'r') as read_file:
            data = json.load(read_file)

        options = os.listdir(data["tier2_dir"])

        self.runFileStart = ttk.Combobox(self.dataFrame, values=options)
        self.runFileStart.current(0)
        self.runFileStart.grid(row=2, column=0)
        #bindthecombobox
        self.runFileStart.bind("<<ComboboxSelected>>", self.pick_file)

        self.run_table = ttk.Combobox(self.dataFrame, value=[" "])
        self.run_table.grid(row=4, column=0)

        self.bin = Entry(self.spectrumViewerWindow, width=35, borderwidth=5)
        self.bin.grid(row=6, column=0, padx=10, pady=10)

        self.my_button = Button(self.dataFrame, text = "Graph It!", command=lambda: self.graphSingle(self.runFileStart.get(), str(self.run_table.get()), int(self.bin.get()))).grid(row=0, column=0)
        self.mylbl = Label(self.dataFrame, text = "What run number would you like to browse?").grid(row=1, column=0)
        self.mylbl2 = Label(self.dataFrame, text = "What table would you like to browse?").grid(row=3, column=0)
        self.mylbl3 = Label(self.dataFrame, text = "What Binning would you like?").grid(row=5, column=0)

        #creating the Menu

        #my_menu = Menu(self.spectrumViewerWindow)
        #self.spectrumViewerWindow.config(menu=my_menu)


        #create a menu item

        #file_menu = Menu(my_menu)
        #my_menu.add_cascade(label="File", menu=file_menu)
        #file_menu.add_command(label="Use Multiple File", command=self.Multi_File)
        #file_menu.add_separator()
        #file_menu.add_command(label="Use Single File", command=self.Single_File)


    def graphSingle(self, fileName, table, bin):
        plt.clf()
        self.fig = Figure(figsize = (5,5) , dpi = 100)
        df = fd.get_df(str(fileName[3:7]), table)

        plot1 = self.fig.add_subplot(111)
        plot1.hist(df['trapEmax'], histtype='step', bins=bin)

        self.figure_canvas = FigureCanvasTkAgg(self.fig, self.spectrumViewerWindow)
        self.figure_canvas.draw()
        self.figure_canvas.get_tk_widget().grid(row=0,column=10,rowspan=7,padx=5,pady=2)

        self.toolbar_frame = Frame(self.spectrumViewerWindow)
        self.toolbar = NavigationToolbar2Tk(self.figure_canvas, self.toolbar_frame)
        self.toolbar.update()
        self.toolbar_frame.grid(row=10, column=10, pady=2)

    def graphMultiple(self, startFile, endFile, table, bin):
        plt.clf()

        self.fig = Figure(figsize = (5,5) , dpi = 100)
        run_list = [x for x in range(int(startFile[3:7]), int(endFile[3:7])+1)]
        df = fd.get_df_multiple(run_list, table)

        plot1 = self.fig.add_subplot(111)
        plot1.hist(df['trapEmax'], histtype='step', bins=bin)

        self.figure_canvas = FigureCanvasTkAgg(self.fig, self.spectrumViewerWindow)
        self.figure_canvas.draw()
        self.figure_canvas.get_tk_widget().grid(row=0,column=10,rowspan=7,padx=5,pady=2)

        self.toolbar_frame = Frame(self.spectrumViewerWindow)
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

        with open('address.json', 'r') as read_file:
            data = json.load(read_file)

        options = os.listdir(data["tier1_dir"])

        self.dataFrame = Frame(self.spectrumViewerWindow)
        self.dataFrame.grid(row=0,column=0)

        self.runFileStart = ttk.Combobox(self.dataFrame, values=options)
        self.runFileStart.current(0)
        self.runFileStart.grid(row=2, column=0)
        #bindthecombobox
        self.runFileStart.bind("<<ComboboxSelected>>", self.pick_file)

        self.run_table = ttk.Combobox(self.dataFrame, value=[" "])
        self.run_table.grid(row=4, column=0)

        self.bin = Entry(self.dataFrame, width=35, borderwidth=5)
        self.bin.grid(row=6, column=0, padx=10, pady=10)

        self.my_button = Button(self.dataFrame, text = "Graph It!", command=lambda: self.graphSingle(self.runFileStart.get(), str(self.run_table.get()), int(self.bin.get()))).grid(row=0, column=0)
        self.mylbl = Label(self.dataFrame, text = "What run number would you like to browse?").grid(row=1, column=0)
        self.mylbl2 = Label(self.dataFrame, text = "What table would you like to browse?").grid(row=3, column=0)
        self.mylbl3 = Label(self.dataFrame, text = "What Binning would you like?").grid(row=5, column=0)


        #creating the Menu

        my_menu = Menu(self.spectrumViewerWindow)
        self.spectrumViewerWindow.config(menu=my_menu)


        #create a menu item

        file_menu = Menu(my_menu)
        my_menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Use Multiple File", command=self.Multi_File)
        file_menu.add_command(label="Use Single File", command=self.Single_File)
        file_menu.add_command(label="exit", command=master.quit)

        action_menu = Menu(my_menu)
        my_menu.add_cascade(label="action", menu=action_menu)
        action_menu.add_command(label="calibrate", command=self.set_calibrate)
