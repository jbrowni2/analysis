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


def pick_file(e):
    file = runFile.get()
    tables = fd.get_tables(int(file[3:7]))
    run_table.config(values=tables)
    run_table.current(0)

def next(index, data):
    plt.clf()
    fig = Figure(figsize = (5,5) , dpi = 100)

    numOfImages = len(data[0]["waveform"]["values"].nda)

    if index > (numOfImages - 1):
        index = 0

    statusText = "Image " + str(index+1) + " of " + str(numOfImages)
    status = Label(wfBrowserWindow, text=statusText, bd=1, relief=SUNKEN, anchor=W)
    status.grid(row=9, column=5, columnspan=3, sticky=W+E)

    df = data[0]["waveform"]["values"].nda[index]

    plot1 = fig.add_subplot(111)
    plot1.plot(df)

    canvas = Canvas(wfBrowserWindow, width=700, height=594)
    canvas.grid(row=0, column=100)

    figure_canvas = FigureCanvasTkAgg(fig, wfBrowserWindow)
    figure_canvas.draw()
    figure_canvas.get_tk_widget().grid(row=0,column=6,rowspan=7,padx=5,pady=2)

    toolbar_frame = Frame(canvas)
    toolbar = NavigationToolbar2Tk(figure_canvas, toolbar_frame)
    toolbar.update()
    toolbar_frame.grid(row=9, column=6, pady=2)

    button_back = Button(wfBrowserWindow, text="<<", command=lambda: back(index-1, data))
    button_next = Button(wfBrowserWindow, text=">>", command=lambda: next(index+1, data))
    button_quit = Button(wfBrowserWindow, text="Exit Program", command=wfBrowserWindow.quit)
    button_quit.grid(row=8, column=6)
    button_back.grid(row=8, column=5)
    button_next.grid(row=8, column=7)

def back(index, data):
    plt.clf()
    fig = Figure(figsize = (5,5) , dpi = 100)

    numOfImages = len(data[0]["waveform"]["values"].nda)

    if index < 0:
        index = numOfImages - 1

    statusText = "Image " + str(index+1) + " of " + str(numOfImages)
    status = Label(wfBrowserWindow, text=statusText, bd=1, relief=SUNKEN, anchor=W)
    status.grid(row=9, column=5, columnspan=3, sticky=W+E)

    df = data[0]["waveform"]["values"].nda[index]

    plot1 = fig.add_subplot(111)
    plot1.plot(df)

    canvas = Canvas(wfBrowserWindow, width=700, height=594)
    canvas.grid(row=0, column=100)

    figure_canvas = FigureCanvasTkAgg(fig, wfBrowserWindow)
    figure_canvas.draw()
    figure_canvas.get_tk_widget().grid(row=0,column=6,rowspan=7,padx=5,pady=2)

    toolbar_frame = Frame(canvas)
    toolbar = NavigationToolbar2Tk(figure_canvas, toolbar_frame)
    toolbar.update()
    toolbar_frame.grid(row=9, column=6, pady=2)

    button_back = Button(wfBrowserWindow, text="<<", command=lambda: back(index-1, data))
    button_next = Button(wfBrowserWindow, text=">>", command=lambda: next(index+1, data))
    button_quit = Button(wfBrowserWindow, text="Exit Program", command=wfBrowserWindow.quit)
    button_quit.grid(row=8, column=6)
    button_back.grid(row=8, column=5)
    button_next.grid(row=8, column=7)



def graph(fileName, table):
    plt.clf()
    fig = Figure(figsize = (5,5) , dpi = 100)
    t1_data = fd.get_t1_data(str(fileName[3:7]), table)

    numOfImages = len(t1_data[0]["waveform"]["values"].nda)

    statusText = "Image 1 of " + str(numOfImages)

    status = Label(wfBrowserWindow, text=statusText, bd=1, relief=SUNKEN, anchor=W)
    status.grid(row=9, column=5, columnspan=3, sticky=W+E)

    df = t1_data[0]["waveform"]["values"].nda[0]

    plot1 = fig.add_subplot(111)
    plot1.plot(df)

    canvas = Canvas(wfBrowserWindow, width=700, height=594)
    canvas.grid(row=0, column=100)

    figure_canvas = FigureCanvasTkAgg(fig, wfBrowserWindow)
    figure_canvas.draw()
    figure_canvas.get_tk_widget().grid(row=0,column=6,rowspan=7,padx=5,pady=2)

    toolbar_frame = Frame(canvas)
    toolbar = NavigationToolbar2Tk(figure_canvas, toolbar_frame)
    toolbar.update()
    toolbar_frame.grid(row=9, column=6, pady=2)

    button_back = Button(wfBrowserWindow, text="<<", command=lambda: back(numOfImages-1, t1_data))
    button_next = Button(wfBrowserWindow, text=">>", command=lambda: next(1, t1_data))
    button_quit = Button(wfBrowserWindow, text="Exit Program", command=wfBrowserWindow.quit)
    button_quit.grid(row=8, column=6)
    button_back.grid(row=8, column=5)
    button_next.grid(row=8, column=7)




def Browser():
    global wfBrowserWindow
    wfBrowserWindow = Tk()

    # sets the title of the
    # Toplevel widget
    wfBrowserWindow.title("Wf Browser Window")

    # sets the geometry of toplevel
    wfBrowserWindow.geometry("1400x600")

    options = os.listdir("/home/jlb1694/data/raw")

    global runFile
    runFile = ttk.Combobox(wfBrowserWindow, values=options)
    runFile.current(0)
    runFile.grid(row=1, column=0)
    #bindthecombobox
    runFile.bind("<<ComboboxSelected>>", pick_file)

    global run_table
    run_table = ttk.Combobox(wfBrowserWindow, value=[" "])
    run_table.grid(row=3, column=0)

    # A Label widget to show in toplevel

    my_button = Button(wfBrowserWindow, text = "Graph It!", command=lambda: graph(runFile.get(), str(run_table.get()))).grid(row=0, column=0)
    mylbl = Label(wfBrowserWindow, text = "What run number would you like to browse?").grid(row=2, column=0)
    mylbl2 = Label(wfBrowserWindow, text = "What table would you like to browse?").grid(row=4, column=0)
