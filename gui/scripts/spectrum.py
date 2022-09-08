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



class spectrumViewer:

    def clear(self, frame):
        frame.destroy()

    def clearAll(self):
        for widget in self.spectrumViewerWindow.winfo_children():
            widget.destroy()

    def fit(self):
        pass

    def calibrate(self):
        peaks = []
        i = 0
        for min in self.peakMinEntries:
            peaks.append([int(min.get()), int(self.peakMaxEntries[i].get())])
            i+=1

        counts, bins, bars = plt.hist(self.df["trapEmax"], histtype='step', bins=int(self.bin.get()))
        adc = []
        for range in peaks:
            peak_range = hA.find_nearest_bin(bins, range[0]), hA.find_nearest_bin(bins, range[1])
            peak_idx = np.argmax(counts[peak_range[0]:peak_range[1]]) + peak_range[0]
            peak = bins[peak_idx]
            adc.append(peak)

        slope, intercept, r_value, p_value, std_err = stats.linregress(adc,energy)

        print(slope)
        print(intercept)

    def createEntries(self, numPeak):
        self.peakMinEntries = []
        self.peakMaxEntries = []
        self.energyEntries = []
        if numPeak != 0:
            for i in range(int(numPeak)):
                self.peak_min = Entry(self.actionFrame)
                self.peak_min.place(x=10, y=i*20+200)
                self.peakMinEntries.append(self.peak_min)
            for i in range(int(numPeak)):
                self.peak_max = Entry(self.actionFrame)
                self.peak_max.place(x=150, y=i*20+200)
                self.peakMaxEntries.append(self.peak_max)
            for i in range(int(numPeak)):
                self.energy = Entry(self.actionFrame)
                self.energy.place(x=10, y=i*20+300)
                self.energyEntries.append(self.energy)

    def set_calibrate(self):
        self.clear(self.actionFrame)
        self.actionFrame = customtkinter.CTkFrame(self.spectrumViewerWindow, width=370, height=950, fg_color='gray')
        self.actionFrame.place(x=1000,y=20)

        self.actionLbl = customtkinter.CTkLabel(self.actionFrame, text="Action Settings", text_font=('Times', 12), bg_color='gray')
        self.actionLbl.place(x=10, y=20)

        self.outputFrame = customtkinter.CTkFrame(self.actionFrame, width=350, height=280, fg_color='light blue')
        self.outputFrame.place(x=10,y=650)

        self.outputLbl = customtkinter.CTkLabel(self.outputFrame, text="Action Output",
            text_font=('Times', 12), bg_color='light blue')
        self.outputLbl.place(x=20, y=10)
        peakMinEntries = []
        my_entries = []
        self.num_range = customtkinter.CTkEntry(self.actionFrame, width=35, borderwidth=5)
        self.num_range.place(x=10, y=80)
        self.myRangeLabel = customtkinter.CTkLabel(self.actionFrame,
            text = "How many peaks are you fitting?", text_font=('Times', 12), bg_color='gray')
        self.myRangeLabel.place(x=10,y=50)
        self.num_range.insert(0, '0')

        self.add_entries = customtkinter.CTkButton(self.actionFrame, text = "Add Entries!",
            command=lambda: self.createEntries(int(self.num_range.get())))
        self.add_entries.place(x=10, y=120)

        self.calibrate_button = customtkinter.CTkButton(self.actionFrame, text = "Calibrate!",
            command=self.calibrate)
        self.calibrate_button.place(x=50, y=400)






    def pick_file(self, file):
        fileNum = ""
        for m in file:
            if m == 'l':
                break
            if m.isdigit():
                fileNum = fileNum + m
        tables = fd.get_tables(int(fileNum))
        table_var = customtkinter.StringVar(value=tables[0])
        self.run_table.set(tables[0])
        self.run_table.configure(values=tables)

    def Multi_File(self):
        self.clearAll()

        self.plotFrame = customtkinter.CTkFrame(self.spectrumViewerWindow, width=650, height=650, fg_color='gray')
        self.plotFrame.place(x=300,y=20)

        self.plotFrameLbl = customtkinter.CTkLabel(self.plotFrame, text="Waveform Plot",
            text_font=('Times', 12), bg_color='gray')
        self.plotFrameLbl.place(x=250, y=10)

        with open('address.json', 'r') as read_file:
            data = json.load(read_file)

        options = os.listdir(data["tier2_dir"])

        self.dataFrame = customtkinter.CTkFrame(self.spectrumViewerWindow, width=250, height=1000, fg_color='gray')
        self.dataFrame.place(x=0,y=0)

        combobox_var = customtkinter.StringVar(value=options[0])
        self.runFileStart = customtkinter.CTkComboBox(self.dataFrame, values=options
        , variable=combobox_var, command=self.pick_file, text_font=('Times', 12))
        self.runFileStart.place(x=10, y=80)

        combobox_var2 = customtkinter.StringVar(value=options[0])
        self.runFileEnd = customtkinter.CTkComboBox(self.dataFrame, values=options
        , variable=combobox_var2, command=self.pick_file, text_font=('Times', 12))
        self.runFileEnd.place(x=10, y=150)


        self.run_table = customtkinter.CTkComboBox(self.dataFrame, values=[" "], text_font=('Times', 12))
        self.run_table.place(x=10, y=210)

        self.dataLbl = customtkinter.CTkLabel(self.dataFrame, text="Data Handling", text_font=('Times', 12), bg_color='gray')
        self.dataLbl.place(x=20, y=10)

        self.bin = customtkinter.CTkEntry(self.dataFrame, placeholder_text="binning",
                               width=120,
                               height=25,)
        self.bin.place(x=10, y=270)

        self.graph_button = customtkinter.CTkButton(self.dataFrame, text = "Graph It!",
            command=lambda: self.graphMultiple(self.runFileStart.get(), self.runFileEnd.get(),
            str(self.run_table.get()), int(self.bin.get())))
        self.graph_button.place(x=50, y=900)
        self.mylbl = customtkinter.CTkLabel(self.dataFrame, text = "What run number would you like to start?")
        self.mylbl.place(x=10, y=50)
        self.mylbl2 = customtkinter.CTkLabel(self.dataFrame, text = "What table would you like to plot?")
        self.mylbl2.place(x=10, y=180)
        self.mylbl3 = customtkinter.CTkLabel(self.dataFrame, text = "What Binning would you like?")
        self.mylbl3.place(x=10, y=240)
        self.mylbl4 = customtkinter.CTkLabel(self.dataFrame, text = "What run number would you like to end?")
        self.mylbl4.place(x=10, y=120)

        #creating the Menu

        my_menu = Menu(self.spectrumViewerWindow)
        self.spectrumViewerWindow.config(menu=my_menu)


        #create a menu item

        file_menu = Menu(my_menu)
        my_menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Use Multiple File", command=self.Multi_File)
        file_menu.add_command(label="Use Single File", command=self.Single_File)
        file_menu.add_command(label="exit", command=self.spectrumViewerWindow.quit)

        action_menu = Menu(my_menu)
        my_menu.add_cascade(label="action", menu=action_menu)
        action_menu.add_command(label="calibrate", command=self.set_calibrate)

        #create the filter frame
        self.filterFrame = customtkinter.CTkFrame(self.spectrumViewerWindow, width=650, height=250, fg_color='gray')
        self.filterFrame.place(x=300,y=700)

        self.filterLbl = customtkinter.CTkLabel(self.filterFrame, text="Filter Settings", text_font=('Times', 12), bg_color='gray')
        self.filterLbl.place(x=10, y=20)

        #create the action frame
        self.actionFrame = customtkinter.CTkFrame(self.spectrumViewerWindow, width=370, height=950, fg_color='gray')
        self.actionFrame.place(x=1000,y=20)

        self.actionLbl = customtkinter.CTkLabel(self.actionFrame, text="Action Settings", text_font=('Times', 12), bg_color='gray')
        self.actionLbl.place(x=10, y=20)

        self.outputFrame = customtkinter.CTkFrame(self.actionFrame, width=350, height=280, fg_color='light blue')
        self.outputFrame.place(x=10,y=650)

        self.outputLbl = customtkinter.CTkLabel(self.outputFrame, text="Action Output", text_font=('Times', 12), bg_color='light blue')
        self.outputLbl.place(x=20, y=10)


    def Single_File(self):
        self.clearAll()

        self.plotFrame = customtkinter.CTkFrame(self.spectrumViewerWindow, width=650, height=650, fg_color='gray')
        self.plotFrame.place(x=300,y=20)

        self.plotFrameLbl = customtkinter.CTkLabel(self.plotFrame, text="Waveform Plot",
            text_font=('Times', 12), bg_color='gray')
        self.plotFrameLbl.place(x=250, y=10)

        with open('address.json', 'r') as read_file:
            data = json.load(read_file)

        options = os.listdir(data["tier2_dir"])

        self.dataFrame = customtkinter.CTkFrame(self.spectrumViewerWindow, width=250, height=1000, fg_color='gray')
        self.dataFrame.place(x=0,y=0)

        combobox_var = customtkinter.StringVar(value=options[0])
        self.runFileStart = customtkinter.CTkComboBox(self.dataFrame, values=options
        , variable=combobox_var, command=self.pick_file, text_font=('Times', 12))
        self.runFileStart.place(x=10, y=80)


        self.run_table = customtkinter.CTkComboBox(self.dataFrame, values=[" "], text_font=('Times', 12))
        self.run_table.place(x=10, y=150)

        self.dataLbl = customtkinter.CTkLabel(self.dataFrame, text="Data Handling", text_font=('Times', 12), bg_color='gray')
        self.dataLbl.place(x=20, y=10)

        self.bin = customtkinter.CTkEntry(self.dataFrame, placeholder_text="binning",
                               width=120,
                               height=25,)
        self.bin.place(x=10, y=210)

        self.graph_button = customtkinter.CTkButton(self.dataFrame, text = "Graph It!",
            command=lambda: self.graphSingle(self.runFileStart.get(), str(self.run_table.get()),
            int(self.bin.get())))
        self.graph_button.place(x=50, y=900)
        self.mylbl = customtkinter.CTkLabel(self.dataFrame, text = "What run number would you like to plot?")
        self.mylbl.place(x=10, y=50)
        self.mylbl2 = customtkinter.CTkLabel(self.dataFrame, text = "What table would you like to plot?")
        self.mylbl2.place(x=10, y=120)
        self.mylbl3 = customtkinter.CTkLabel(self.dataFrame, text = "What Binning would you like?")
        self.mylbl3.place(x=10, y=180)

        #creating the Menu

        my_menu = Menu(self.spectrumViewerWindow)
        self.spectrumViewerWindow.config(menu=my_menu)


        #create a menu item

        file_menu = Menu(my_menu)
        my_menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Use Multiple File", command=self.Multi_File)
        file_menu.add_command(label="Use Single File", command=self.Single_File)
        file_menu.add_command(label="exit", command=self.spectrumViewerWindow.quit)

        action_menu = Menu(my_menu)
        my_menu.add_cascade(label="action", menu=action_menu)
        action_menu.add_command(label="calibrate", command=self.set_calibrate)

        #create the filter frame
        self.filterFrame = customtkinter.CTkFrame(self.spectrumViewerWindow, width=650, height=250, fg_color='gray')
        self.filterFrame.place(x=300,y=700)

        self.filterLbl = customtkinter.CTkLabel(self.filterFrame, text="Filter Settings", text_font=('Times', 12), bg_color='gray')
        self.filterLbl.place(x=10, y=20)

        #create the action frame
        self.actionFrame = customtkinter.CTkFrame(self.spectrumViewerWindow, width=370, height=950, fg_color='gray')
        self.actionFrame.place(x=1000,y=20)

        self.actionLbl = customtkinter.CTkLabel(self.actionFrame, text="Action Settings", text_font=('Times', 12), bg_color='gray')
        self.actionLbl.place(x=10, y=20)

        self.outputFrame = customtkinter.CTkFrame(self.actionFrame, width=350, height=280, fg_color='light blue')
        self.outputFrame.place(x=10,y=650)

        self.outputLbl = customtkinter.CTkLabel(self.outputFrame, text="Action Output", text_font=('Times', 12), bg_color='light blue')
        self.outputLbl.place(x=20, y=10)


    def graphSingle(self, fileName, table, bin):
        plt.clf()
        self.fig = Figure(figsize = (5,5) , dpi = 100)
        fileNum = ""
        for m in fileName:
            if m == 'l':
                break
            if m.isdigit():
                fileNum = fileNum + m
        self.df = fd.get_df(str(fileNum), table)

        plot1 = self.fig.add_subplot(111)
        plot1.hist(self.df['trapEmax'], histtype='step', bins=bin)

        figure_canvas = FigureCanvasTkAgg(self.fig, self.plotFrame)
        figure_canvas.draw()
        figure_canvas.get_tk_widget().place(x=80, y=50)

        toolbar_frame = Frame(self.plotFrame)
        toolbar = NavigationToolbar2Tk(figure_canvas, toolbar_frame)
        toolbar.update()
        toolbar_frame.place(x=200, y=580)

    def graphMultiple(self, startFile, endFile, table, bin):
        plt.clf()

        self.fig = Figure(figsize = (5,5) , dpi = 100)
        fileStartNum = ""
        for m in startFile:
            if m == 'l':
                break
            if m.isdigit():
                fileStartNum = fileStartNum + m


        fileEndNum = ""
        for m in endFile:
            if m == 'l':
                break
            if m.isdigit():
                fileEndNum = fileEndNum + m

        run_list = [x for x in range(int(fileStartNum), int(fileEndNum)+1)]
        df = fd.get_df_multiple(run_list, table)

        plot1 = self.fig.add_subplot(111)
        plot1.hist(df['trapEmax'], histtype='step', bins=bin)

        figure_canvas = FigureCanvasTkAgg(self.fig, self.plotFrame)
        figure_canvas.draw()
        figure_canvas.get_tk_widget().place(x=80, y=50)

        toolbar_frame = Frame(self.plotFrame)
        toolbar = NavigationToolbar2Tk(figure_canvas, toolbar_frame)
        toolbar.update()
        toolbar_frame.place(x=200, y=580)

    def __init__(self, master):

        self.spectrumViewerWindow = customtkinter.CTkToplevel()
        self.spectrumViewerWindow.configure(bg='gray20')

        # sets the title of the
        # Toplevel widget
        self.spectrumViewerWindow.title("Energy Spectrum Window")

        # sets the geometry of toplevel
        self.spectrumViewerWindow.geometry("1400x1000")

        self.plotFrame = customtkinter.CTkFrame(self.spectrumViewerWindow, width=650, height=650, fg_color='gray')
        self.plotFrame.place(x=300,y=20)

        self.plotFrameLbl = customtkinter.CTkLabel(self.plotFrame, text="Waveform Plot",
            text_font=('Times', 12), bg_color='gray')
        self.plotFrameLbl.place(x=250, y=10)

        with open('address.json', 'r') as read_file:
            data = json.load(read_file)

        options = os.listdir(data["tier2_dir"])

        self.dataFrame = customtkinter.CTkFrame(self.spectrumViewerWindow, width=250, height=1000, fg_color='gray')
        self.dataFrame.place(x=0,y=0)

        combobox_var = customtkinter.StringVar(value=options[0])
        self.runFileStart = customtkinter.CTkComboBox(self.dataFrame, values=options
        , variable=combobox_var, command=self.pick_file, text_font=('Times', 12))
        self.runFileStart.place(x=10, y=80)


        self.run_table = customtkinter.CTkComboBox(self.dataFrame, values=[" "], text_font=('Times', 12))
        self.run_table.place(x=10, y=150)

        self.dataLbl = customtkinter.CTkLabel(self.dataFrame, text="Data Handling", text_font=('Times', 12), bg_color='gray')
        self.dataLbl.place(x=20, y=10)

        self.bin = customtkinter.CTkEntry(self.dataFrame, placeholder_text="binning",
                               width=120,
                               height=25,)
        self.bin.place(x=10, y=210)

        self.graph_button = customtkinter.CTkButton(self.dataFrame, text = "Graph It!",
            command=lambda: self.graphSingle(self.runFileStart.get(), str(self.run_table.get()),
            int(self.bin.get())))
        self.graph_button.place(x=50, y=500)
        self.mylbl = customtkinter.CTkLabel(self.dataFrame, text = "What run number would you like to plot?")
        self.mylbl.place(x=10, y=50)
        self.mylbl2 = customtkinter.CTkLabel(self.dataFrame, text = "What table would you like to plot?")
        self.mylbl2.place(x=10, y=120)
        self.mylbl3 = customtkinter.CTkLabel(self.dataFrame, text = "What Binning would you like?")
        self.mylbl3.place(x=10, y=180)


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


        #create the filter frame
        self.filterFrame = customtkinter.CTkFrame(self.spectrumViewerWindow, width=650, height=250, fg_color='gray')
        self.filterFrame.place(x=300,y=700)

        self.filterLbl = customtkinter.CTkLabel(self.filterFrame, text="Filter Settings", text_font=('Times', 12), bg_color='gray')
        self.filterLbl.place(x=10, y=20)

        #create the action frame
        self.actionFrame = customtkinter.CTkFrame(self.spectrumViewerWindow, width=370, height=950, fg_color='gray')
        self.actionFrame.place(x=1000,y=20)

        self.actionLbl = customtkinter.CTkLabel(self.actionFrame, text="Action Settings", text_font=('Times', 12), bg_color='gray')
        self.actionLbl.place(x=10, y=20)

        self.outputFrame = customtkinter.CTkFrame(self.actionFrame, width=350, height=280, fg_color='light blue')
        self.outputFrame.place(x=10,y=650)

        self.outputLbl = customtkinter.CTkLabel(self.outputFrame, text="Action Output", text_font=('Times', 12), bg_color='light blue')
        self.outputLbl.place(x=20, y=10)
