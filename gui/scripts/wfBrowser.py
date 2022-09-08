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


customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

def clear(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def pick_file(file):
    fileNum = ""
    for m in file:
        if m == 'l':
            break
        if m.isdigit():
            fileNum = fileNum + m
    tables = fd.get_tables(int(fileNum))
    table_var = customtkinter.StringVar(value=tables[0])
    run_table.set(tables[0])
    run_table.configure(values=tables)


def next(index, data):
    plt.clf()

    clear(plotFrame)
    plotFrameLbl = customtkinter.CTkLabel(plotFrame, text="Waveform Plot", text_font=('Times', 12), bg_color='gray')
    plotFrameLbl.place(x=250, y=10)

    fig = Figure(figsize = (5,5) , dpi = 100)

    numOfImages = len(data[0]["waveform"]["values"].nda)

    if index > numOfImages-1:
        index = 0

    channelCheck = channelFilter.get()

    if channelCheck != "any":
        while data[0]["channel"].nda[index] != int(channelCheck):
            index += 1
            if index > numOfImages-1:
                index = 0

    statusText = "Image " + str(index+1) + " of " + str(numOfImages)

    status = Label(plotFrame, text=statusText, bd=1, relief=SUNKEN, anchor=W)
    status.place(x=260, y=550)

    df = pd.DataFrame(data[0]["waveform"]["values"].nda[index]).T

    if blSwitch.get() == "on":
        df = df - np.mean(df.iloc[0][0:1000])

    plot1 = fig.add_subplot(111)
    plot1.plot(df.iloc[0])

    figure_canvas = FigureCanvasTkAgg(fig, plotFrame)
    figure_canvas.draw()
    figure_canvas.get_tk_widget().place(x=80, y=50)

    toolbar_frame = Frame(plotFrame)
    toolbar = NavigationToolbar2Tk(figure_canvas, toolbar_frame)
    toolbar.update()
    toolbar_frame.place(x=200, y=580)

    button_back = customtkinter.CTkButton(plotFrame, text="<<", command=lambda: back(index-1, data))
    button_next = customtkinter.CTkButton(plotFrame, text=">>", command=lambda: next(index+1, data))
    button_quit = customtkinter.CTkButton(plotFrame, text="Exit Program", command=wfBrowserWindow.quit)
    button_quit.place(x=250, y=650)
    button_back.place(x=20, y=650)
    button_next.place(x=480, y=650)

    #findRms
    rms = hA.findRms(df.iloc[0])
    rmsLbl1 = customtkinter.CTkLabel(calculationFrame, text="RMS:", text_font=('Times', 12), bg_color='white')
    rmsLbl1.place(x=-40, y=50)
    rmsLbl2 = customtkinter.CTkLabel(calculationFrame, text=str(rms), text_font=('Times', 12), bg_color='white')
    rmsLbl2.place(x=60, y=50)
    rmsLbl3 = customtkinter.CTkLabel(calculationFrame, text="ADC", text_font=('Times', 12),
        bg_color='white', width=40)
    rmsLbl3.place(x=220, y=50)

    timestampLbl1 = customtkinter.CTkLabel(calculationFrame, text="Timestamp:", text_font=('Times', 12),
        bg_color='white', width=80)
    timestampLbl1.place(x=5, y=80)
    timestampLbl2 = customtkinter.CTkLabel(calculationFrame, text=str(data[0]["timestamp"].nda[index]),
        text_font=('Times', 12), bg_color='white', width=120)
    timestampLbl2.place(x=90, y=80)
    timestampLbl3 = customtkinter.CTkLabel(calculationFrame, text="Clock Units",
        text_font=('Times', 12), bg_color='white', width=80)
    timestampLbl3.place(x=220, y=80)


def back(index, data):
    plt.clf()
    clear(plotFrame)
    plotFrameLbl = customtkinter.CTkLabel(plotFrame, text="Waveform Plot", text_font=('Times', 12), bg_color='gray')
    plotFrameLbl.place(x=250, y=10)

    fig = Figure(figsize = (5,5) , dpi = 100)

    numOfImages = len(data[0]["waveform"]["values"].nda)

    if index < 0:
        index = numOfImages-1

    channelCheck = channelFilter.get()

    if channelCheck != "any":
        while data[0]["channel"].nda[index] != int(channelCheck):
            index -= 1
            if index < 0:
                index = numOfImages-1

    statusText = "Image " + str(index+1) + " of " + str(numOfImages)

    status = Label(plotFrame, text=statusText, bd=1, relief=SUNKEN, anchor=W)
    status.place(x=260, y=550)


    df = pd.DataFrame(data[0]["waveform"]["values"].nda[index]).T

    if blSwitch.get() == "on":
        df = df - np.mean(df.iloc[0][0:1000])

    plot1 = fig.add_subplot(111)
    plot1.plot(df.iloc[0])

    figure_canvas = FigureCanvasTkAgg(fig, plotFrame)
    figure_canvas.draw()
    figure_canvas.get_tk_widget().place(x=80, y=50)

    toolbar_frame = Frame(plotFrame)
    toolbar = NavigationToolbar2Tk(figure_canvas, toolbar_frame)
    toolbar.update()
    toolbar_frame.place(x=200, y=580)

    button_back = customtkinter.CTkButton(plotFrame, text="<<", command=lambda: back(index-1, data))
    button_next = customtkinter.CTkButton(plotFrame, text=">>", command=lambda: next(index+1, data))
    button_quit = customtkinter.CTkButton(plotFrame, text="Exit Program", command=wfBrowserWindow.quit)
    button_quit.place(x=250, y=650)
    button_back.place(x=20, y=650)
    button_next.place(x=480, y=650)

    #findRms
    rms = hA.findRms(df.iloc[0])
    rmsLbl1 = customtkinter.CTkLabel(calculationFrame, text="RMS:", text_font=('Times', 12), bg_color='white')
    rmsLbl1.place(x=-40, y=50)
    rmsLbl2 = customtkinter.CTkLabel(calculationFrame, text=str(rms), text_font=('Times', 12), bg_color='white')
    rmsLbl2.place(x=60, y=50)
    rmsLbl3 = customtkinter.CTkLabel(calculationFrame, text="ADC", text_font=('Times', 12),
        bg_color='white', width=40)
    rmsLbl3.place(x=220, y=50)

    timestampLbl1 = customtkinter.CTkLabel(calculationFrame, text="Timestamp:", text_font=('Times', 12),
        bg_color='white', width=80)
    timestampLbl1.place(x=5, y=80)
    timestampLbl2 = customtkinter.CTkLabel(calculationFrame, text=str(data[0]["timestamp"].nda[index]),
        text_font=('Times', 12), bg_color='white', width=120)
    timestampLbl2.place(x=90, y=80)
    timestampLbl3 = customtkinter.CTkLabel(calculationFrame, text="Clock Units",
        text_font=('Times', 12), bg_color='white', width=80)
    timestampLbl3.place(x=220, y=80)



def graph(fileName, table):
    plt.clf()
    global plotFrame
    plotFrame = customtkinter.CTkFrame(wfBrowserWindow, width=650, height=700, fg_color='gray')
    plotFrame.place(x=300,y=20)
    plotFrameLbl = customtkinter.CTkLabel(plotFrame, text="Waveform Plot", text_font=('Times', 12), bg_color='gray')
    plotFrameLbl.place(x=250, y=10)

    fig = Figure(figsize = (5,5) , dpi = 100)
    fileNum = ""
    for m in fileName:
        if m == 'l':
            break
        if m.isdigit():
            fileNum = fileNum + m
    t1_data = fd.get_t1_data(str(fileNum), table)

    numOfImages = len(t1_data[0]["waveform"]["values"].nda)

    statusText = "Image 1 of " + str(numOfImages)

    status = Label(plotFrame, text=statusText, bd=1, relief=SUNKEN, anchor=W)
    status.place(x=260, y=550)


    channels = list(map(str, np.unique(t1_data[0]["channel"].nda)))
    channels.append("any")
    channelFilter.set(channels[-1])
    channelFilter.configure(values=channels)

    df = pd.DataFrame(t1_data[0]["waveform"]["values"].nda[0]).T

    if blSwitch.get() == "on":
        df = df - np.mean(df.iloc[0][0:1000])

    plot1 = fig.add_subplot(111)
    plot1.plot(df.iloc[0])

    figure_canvas = FigureCanvasTkAgg(fig, plotFrame)
    figure_canvas.draw()
    figure_canvas.get_tk_widget().place(x=80, y=50)

    toolbar_frame = Frame(plotFrame)
    toolbar = NavigationToolbar2Tk(figure_canvas, toolbar_frame)
    toolbar.update()
    toolbar_frame.place(x=200, y=580)

    button_back = customtkinter.CTkButton(plotFrame, text="<<", command=lambda: back(numOfImages-1, t1_data))
    button_next = customtkinter.CTkButton(plotFrame, text=">>", command=lambda: next(1, t1_data))
    button_quit = customtkinter.CTkButton(plotFrame, text="Exit Program", command=wfBrowserWindow.quit)
    button_quit.place(x=250, y=650)
    button_back.place(x=20, y=650)
    button_next.place(x=480, y=650)

    #findRms
    rms = hA.findRms(df.iloc[0])
    rmsLbl1 = customtkinter.CTkLabel(calculationFrame, text="RMS:", text_font=('Times', 12), bg_color='white')
    rmsLbl1.place(x=-40, y=50)
    rmsLbl2 = customtkinter.CTkLabel(calculationFrame, text=str(rms), text_font=('Times', 12), bg_color='white')
    rmsLbl2.place(x=60, y=50)
    rmsLbl3 = customtkinter.CTkLabel(calculationFrame, text="ADC", text_font=('Times', 12),
        bg_color='white', width=40)
    rmsLbl3.place(x=220, y=50)


    timestampLbl1 = customtkinter.CTkLabel(calculationFrame, text="Timestamp:", text_font=('Times', 12),
        bg_color='white', width=80)
    timestampLbl1.place(x=5, y=80)
    timestampLbl2 = customtkinter.CTkLabel(calculationFrame, text=str(t1_data[0]["timestamp"].nda[0]),
        text_font=('Times', 12), bg_color='white', width=120)
    timestampLbl2.place(x=90, y=80)
    timestampLbl3 = customtkinter.CTkLabel(calculationFrame, text="Clock Units",
        text_font=('Times', 12), bg_color='white', width=80)
    timestampLbl3.place(x=220, y=80)





def Browser():
    global wfBrowserWindow
    wfBrowserWindow = customtkinter.CTkToplevel()
    wfBrowserWindow.configure(bg='gray20')

    # sets the title of the
    # Toplevel widget
    wfBrowserWindow.title("Wf Browser Window")

    # sets the geometry of toplevel
    wfBrowserWindow.geometry("1400x800")

    plotFrame = customtkinter.CTkFrame(wfBrowserWindow, width=650, height=700, fg_color='gray')
    plotFrame.place(x=300,y=20)

    plotFrameLbl = customtkinter.CTkLabel(plotFrame, text="Waveform Plot", text_font=('Times', 12), bg_color='gray')
    plotFrameLbl.place(x=250, y=10)

    with open('address.json', 'r') as read_file:
        data = json.load(read_file)

    options = os.listdir(data["tier1_dir"])

    dataFrame = customtkinter.CTkFrame(wfBrowserWindow, width=250, height=1000, fg_color='gray')
    dataFrame.place(x=0,y=0)

    global runFile
    combobox_var = customtkinter.StringVar(value=options[0])
    runFile = customtkinter.CTkComboBox(dataFrame, values=options, variable=combobox_var, command=pick_file, text_font=('Times', 12))
    runFile.place(x=10, y=70)

    global run_table
    run_table = customtkinter.CTkComboBox(dataFrame, values=[" "], text_font=('Times', 12))
    run_table.place(x=10, y=150)

    dataLbl = customtkinter.CTkLabel(dataFrame, text="Data Handling", text_font=('Times', 12), bg_color='gray')
    dataLbl.place(x=20, y=10)

    #adding the filters and the calculations
    filterFrame = customtkinter.CTkFrame(wfBrowserWindow, width=350, height=350, fg_color='gray')
    filterFrame.place(x=1000,y=20)

    filterLbl = customtkinter.CTkLabel(filterFrame, text="Waveform Filters", text_font=('Times', 12), bg_color='gray')
    filterLbl.place(x=20, y=10)

    global calculationFrame
    calculationFrame = customtkinter.CTkFrame(wfBrowserWindow, width=350, height=350, fg_color='white')
    calculationFrame.place(x=1000,y=400)

    calculationLbl = customtkinter.CTkLabel(calculationFrame, text="Waveform Calculations", text_font=('Times', 12), bg_color='white')
    calculationLbl.place(x=20, y=10)

    blSwitch_var = customtkinter.StringVar(value="off")

    global blSwitch
    blSwitch = customtkinter.CTkSwitch(master=filterFrame, text="Baseline Subtraction",
            variable=blSwitch_var, onvalue="on", offvalue="off")
    blSwitch.place(x=10, y=325)

    global channelFilter
    channelFilter = customtkinter.CTkComboBox(filterFrame, values=["Pick Channel"], text_font=('Times', 12))
    channelFilter.place(x=10, y=50)


    my_button = customtkinter.CTkButton(dataFrame, text = "Graph It!", text_font=('Times', 12), text_color=("black", "white"), fg_color="white", command=lambda: graph(runFile.get(), str(run_table.get())))
    my_button.place(x=10, y=700)
    mylbl = customtkinter.CTkLabel(dataFrame, text = "What run number would you like?", text_font=('Times', 12), text_color="black")
    mylbl.place(x=10, y=40)
    mylbl2 = customtkinter.CTkLabel(dataFrame, text = "What table would you like?", text_font=('Times', 12), text_color="black")
    mylbl2.place(x=10, y=120)
