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
import scipy.signal as sig

from wfBase import waveBrowse


customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


def graph(fileName, table, window):
    plt.clf()

    fig = Figure(figsize = (5,5) , dpi = 100)
    fileNum = ""
    for m in fileName:
        if m == 'l':
            break
        if m.isdigit():
            fileNum = fileNum + m
    t1_data = fd.get_t1_data(str(fileNum), table)

    numOfImages = len(t1_data[0]["waveform"]["values"].nda)
    time = t1_data[0]["timestamp"].nda

    statusText = "Image 1 of " + str(numOfImages)

    status = Label(wfNormal.plotFrame, text=statusText, bd=1, relief=SUNKEN, anchor=W)
    status.place(x=260, y=550)


    channels = list(map(str, np.unique(t1_data[0]["channel"].nda)))
    channels.append("any")
    wfNormal.channelFilter.set(channels[-1])
    wfNormal.channelFilter.configure(values=channels)

    rise = int(8*1000/8)
    flat = int(0.5*1000/8)

    trapFilter = np.zeros(2*rise + flat)

    trapFilter[0:rise] = 1.0
    trapFilter[rise+1:flat+rise] = 0.0
    trapFilter[rise+flat+1:] = -1.0

    trapWave = np.zeros((len(t1_data[0]["waveform"]["values"].nda), len(t1_data[0]["waveform"]["values"].nda[0])- len(trapFilter)+1))
    for i,wave in enumerate(t1_data[0]["waveform"]["values"].nda):
        trapWave[i] = sig.convolve(wave, trapFilter, "valid")

    df = pd.DataFrame(trapWave[0]).T

    if wfNormal.blSwitch.get() == "on":
        df = df - np.mean(df.iloc[0][0:1000])


    plot1 = fig.add_subplot(111)
    plot1.plot(df.iloc[0])

    figure_canvas = FigureCanvasTkAgg(fig, wfNormal.plotFrame)
    figure_canvas.draw()
    figure_canvas.get_tk_widget().place(x=80, y=50)

    toolbar_frame = Frame(wfNormal.plotFrame)
    toolbar = NavigationToolbar2Tk(figure_canvas, toolbar_frame)
    toolbar.update()
    toolbar_frame.place(x=200, y=580)

    button_back = customtkinter.CTkButton(wfNormal.plotFrame, text="<<", command=lambda: wfNormal.back(numOfImages-1, trapWave,
         window, numOfImages, time))
    button_next = customtkinter.CTkButton(wfNormal.plotFrame, text=">>", command=lambda: wfNormal.next(1, trapWave, 
        window, numOfImages, time))
    button_quit = customtkinter.CTkButton(wfNormal.plotFrame, text="Exit Program", command=window.quit)
    button_quit.place(x=250, y=650)
    button_back.place(x=20, y=650)
    button_next.place(x=480, y=650)

    #findRms
    rms = hA.findRms(df.iloc[0])
    rmsLbl1 = customtkinter.CTkLabel(wfNormal.calculationFrame, text="RMS:", text_font=('Times', 12), bg_color='light blue')
    rmsLbl1.place(x=-40, y=50)
    rmsLbl2 = customtkinter.CTkLabel(wfNormal.calculationFrame, text=str(rms), text_font=('Times', 12), bg_color='light blue')
    rmsLbl2.place(x=60, y=50)
    rmsLbl3 = customtkinter.CTkLabel(wfNormal.calculationFrame, text="ADC", text_font=('Times', 12),
        bg_color='light blue', width=40)
    rmsLbl3.place(x=220, y=50)


    timestampLbl1 = customtkinter.CTkLabel(wfNormal.calculationFrame, text="Timestamp:", text_font=('Times', 12),
        bg_color='light blue', width=80)
    timestampLbl1.place(x=5, y=80)
    timestampLbl2 = customtkinter.CTkLabel(wfNormal.calculationFrame, text=str(time[0]),
        text_font=('Times', 12), bg_color='light blue', width=120)
    timestampLbl2.place(x=90, y=80)
    timestampLbl3 = customtkinter.CTkLabel(wfNormal.calculationFrame, text="Clock Units",
        text_font=('Times', 12), bg_color='light blue', width=80)
    timestampLbl3.place(x=220, y=80)



def trapFiltered(window):
    global wfNormal
    wfNormal = waveBrowse(window)

    my_button = customtkinter.CTkButton(wfNormal.dataFrame, text = "Graph It!", text_font=('Times', 12), text_color=("black", "light blue"), 
        fg_color="light blue", command=lambda: graph(wfNormal.runFile.get(), str(wfNormal.run_table.get()), window))
    my_button.place(x=10, y=700)