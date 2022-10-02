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

class waveBrowse:

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

    def clear(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def next(self, index, data, window, numOfImages, time):
        plt.clf()

        self.clear(self.plotFrame)
        plotFrameLbl = customtkinter.CTkLabel(self.plotFrame, text="Waveform Plot", text_font=('Times', 12), bg_color='gray')
        plotFrameLbl.place(x=250, y=10)

        fig = Figure(figsize = (5,5) , dpi = 100)


        if index > numOfImages-1:
            index = 0

        channelCheck = self.channelFilter.get()

        if channelCheck != "any":
            while data[0]["channel"].nda[index] != int(channelCheck):
                index += 1
                if index > numOfImages-1:
                    index = 0

        statusText = "Image " + str(index+1) + " of " + str(numOfImages)

        status = Label(self.plotFrame, text=statusText, bd=1, relief=SUNKEN, anchor=W)
        status.place(x=260, y=550)

        df = pd.DataFrame(data[index]).T

        if self.blSwitch.get() == "on":
            df = df - np.mean(df.iloc[0][0:1000])

        plot1 = fig.add_subplot(111)
        plot1.plot(df.iloc[0])

        figure_canvas = FigureCanvasTkAgg(fig, self.plotFrame)
        figure_canvas.draw()
        figure_canvas.get_tk_widget().place(x=80, y=50)

        toolbar_frame = Frame(self.plotFrame)
        toolbar = NavigationToolbar2Tk(figure_canvas, toolbar_frame)
        toolbar.update()
        toolbar_frame.place(x=200, y=580)

        button_back = customtkinter.CTkButton(self.plotFrame, text="<<", command=lambda: self.back(index-1, data, window, numOfImages, time))
        button_next = customtkinter.CTkButton(self.plotFrame, text=">>", command=lambda: self.next(index+1, data, window, numOfImages, time))
        button_quit = customtkinter.CTkButton(self.plotFrame, text="Exit Program", command=window.quit)
        button_quit.place(x=250, y=650)
        button_back.place(x=20, y=650)
        button_next.place(x=480, y=650)

        #findRms
        rms = hA.findRms(df.iloc[0])
        rmsLbl1 = customtkinter.CTkLabel(self.calculationFrame, text="RMS:", text_font=('Times', 12), bg_color='light blue')
        rmsLbl1.place(x=-40, y=50)
        rmsLbl2 = customtkinter.CTkLabel(self.calculationFrame, text=str(rms), text_font=('Times', 12), bg_color='light blue')
        rmsLbl2.place(x=60, y=50)
        rmsLbl3 = customtkinter.CTkLabel(self.calculationFrame, text="ADC", text_font=('Times', 12),
            bg_color='light blue', width=40)
        rmsLbl3.place(x=220, y=50)

        timestampLbl1 = customtkinter.CTkLabel(self.calculationFrame, text="Timestamp:", text_font=('Times', 12),
            bg_color='light blue', width=80)
        timestampLbl1.place(x=5, y=80)
        timestampLbl2 = customtkinter.CTkLabel(self.calculationFrame, text=str(time[index]),
            text_font=('Times', 12), bg_color='light blue', width=120)
        timestampLbl2.place(x=90, y=80)
        timestampLbl3 = customtkinter.CTkLabel(self.calculationFrame, text="Clock Units",
            text_font=('Times', 12), bg_color='light blue', width=80)
        timestampLbl3.place(x=220, y=80)


    def back(self, index, data, window, numOfImages, time):
        plt.clf()
        self.clear(self.plotFrame)
        plotFrameLbl = customtkinter.CTkLabel(self.plotFrame, text="Waveform Plot", text_font=('Times', 12), bg_color='gray')
        plotFrameLbl.place(x=250, y=10)

        fig = Figure(figsize = (5,5) , dpi = 100)

        if index < 0:
            index = numOfImages-1

        channelCheck = self.channelFilter.get()

        if channelCheck != "any":
            while data[0]["channel"].nda[index] != int(channelCheck):
                index -= 1
                if index < 0:
                    index = numOfImages-1

        statusText = "Image " + str(index+1) + " of " + str(numOfImages)

        status = Label(self.plotFrame, text=statusText, bd=1, relief=SUNKEN, anchor=W)
        status.place(x=260, y=550)


        df = pd.DataFrame(data[index]).T

        if self.blSwitch.get() == "on":
            df = df - np.mean(df.iloc[0][0:1000])

        plot1 = fig.add_subplot(111)
        plot1.plot(df.iloc[0])

        figure_canvas = FigureCanvasTkAgg(fig, self.plotFrame)
        figure_canvas.draw()
        figure_canvas.get_tk_widget().place(x=80, y=50)

        toolbar_frame = Frame(self.plotFrame)
        toolbar = NavigationToolbar2Tk(figure_canvas, toolbar_frame)
        toolbar.update()
        toolbar_frame.place(x=200, y=580)

        button_back = customtkinter.CTkButton(self.plotFrame, text="<<", command=lambda: self.back(index-1, data, window, numOfImages, time))
        button_next = customtkinter.CTkButton(self.plotFrame, text=">>", command=lambda: self.next(index+1, data, window, numOfImages, time))
        button_quit = customtkinter.CTkButton(self.plotFrame, text="Exit Program", command=window.quit)
        button_quit.place(x=250, y=650)
        button_back.place(x=20, y=650)
        button_next.place(x=480, y=650)

        #findRms
        rms = hA.findRms(df.iloc[0])
        rmsLbl1 = customtkinter.CTkLabel(self.calculationFrame, text="RMS:", text_font=('Times', 12), bg_color='light blue')
        rmsLbl1.place(x=-40, y=50)
        rmsLbl2 = customtkinter.CTkLabel(self.calculationFrame, text=str(rms), text_font=('Times', 12), bg_color='light blue')
        rmsLbl2.place(x=60, y=50)
        rmsLbl3 = customtkinter.CTkLabel(self.calculationFrame, text="ADC", text_font=('Times', 12),
            bg_color='light blue', width=40)
        rmsLbl3.place(x=220, y=50)

        timestampLbl1 = customtkinter.CTkLabel(self.calculationFrame, text="Timestamp:", text_font=('Times', 12),
            bg_color='light blue', width=80)
        timestampLbl1.place(x=5, y=80)
        timestampLbl2 = customtkinter.CTkLabel(self.calculationFrame, text=str(time[index]),
            text_font=('Times', 12), bg_color='light blue', width=120)
        timestampLbl2.place(x=90, y=80)
        timestampLbl3 = customtkinter.CTkLabel(self.calculationFrame, text="Clock Units",
            text_font=('Times', 12), bg_color='light blue', width=80)
        timestampLbl3.place(x=220, y=80)

    def __init__(self, window):
        self.plotFrame = customtkinter.CTkFrame(window, width=650, height=700, fg_color='gray')
        self.plotFrame.place(x=300,y=20)

        self.plotFrameLbl = customtkinter.CTkLabel(window, text="Waveform Plot", text_font=('Times', 12), bg_color='gray')
        self.plotFrameLbl.place(x=250, y=10)

        with open('address.json', 'r') as read_file:
            data = json.load(read_file)

        options = os.listdir(data["tier1_dir"])

        self.dataFrame = customtkinter.CTkFrame(window, width=250, height=1000, fg_color='gray')
        self.dataFrame.place(x=0,y=0)

        combobox_var = customtkinter.StringVar(value=options[0])
        self.runFile = customtkinter.CTkComboBox(self.dataFrame, values=options
        , variable=combobox_var, command=self.pick_file, text_font=('Times', 12))
        self.runFile.place(x=10, y=80)


        self.run_table = customtkinter.CTkComboBox(self.dataFrame, values=[" "], text_font=('Times', 12))
        self.run_table.place(x=10, y=150)

        self.dataLbl = customtkinter.CTkLabel(self.dataFrame, text="Data Handling", text_font=('Times', 12), bg_color='gray')
        self.dataLbl.place(x=20, y=10)

        self.filterFrame = customtkinter.CTkFrame(window, width=350, height=350, fg_color='gray')
        self.filterFrame.place(x=1000,y=20)

        self.filterLbl = customtkinter.CTkLabel(self.filterFrame, text="Waveform Filters", text_font=('Times', 12), bg_color='gray')
        self.filterLbl.place(x=20, y=10)

        self.calculationFrame = customtkinter.CTkFrame(window, width=350, height=350, fg_color='light blue')
        self.calculationFrame.place(x=1000,y=400)

        self.calculationLbl = customtkinter.CTkLabel(self.calculationFrame, text="Waveform Calculations", text_font=('Times', 12), bg_color='light blue')
        self.calculationLbl.place(x=20, y=10)


        self.blSwitch_var = customtkinter.StringVar(value="off")
        self.blSwitch = customtkinter.CTkSwitch(master=self.filterFrame, text="Baseline Subtraction",
            variable=self.blSwitch_var, onvalue="on", offvalue="off")
        self.blSwitch.place(x=10, y=325)

        self.channelFilter = customtkinter.CTkComboBox(self.filterFrame, values=["Pick Channel"], text_font=('Times', 12))
        self.channelFilter.place(x=10, y=50)

        mylbl = customtkinter.CTkLabel(self.dataFrame, text = "What run number would you like?", text_font=('Times', 12), text_color="black")
        mylbl.place(x=10, y=40)
        mylbl2 = customtkinter.CTkLabel(self.dataFrame, text = "What table would you like?", text_font=('Times', 12), text_color="black")
        mylbl2.place(x=10, y=120)



