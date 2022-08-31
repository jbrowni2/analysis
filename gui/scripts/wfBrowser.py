from tkinter import *
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

def next(index, data):
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



def graph(run):
    fig = Figure(figsize = (5,5) , dpi = 100)
    t1_data = fd.get_t1_data(run, "Card1")

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

    # A Label widget to show in toplevel
    e = Entry(wfBrowserWindow, width=35, borderwidth=5)
    e.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
    my_button = Button(wfBrowserWindow, text = "Graph It!", command=lambda: graph(int(e.get()))).grid(row=0, column=0)
    mylbl = Label(wfBrowserWindow, text = "What run number would you like to browse?").grid(row=2, column=0)
