from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import filedialog
import sys

# adding Folder_2/subfolder to the system path
sys.path.insert(0, '/home/jlb1694/analysis/gui/scripts')

from wfBrowser import Browser
from changeDirectory import *
from spectrum import spectrumViewer

master = Tk()
master.title("Pygama Analysis GUI")
ico = Image.open('images/gamma.png')
photo = ImageTk.PhotoImage(ico)
master.wm_iconphoto(False, photo)
master.geometry("400x400")


photo = PhotoImage(file = "/home/jlb1694/analysis/gui/images/wfBrowser.png")
photoimage = photo.subsample(3, 3)

photo = PhotoImage(file = "/home/jlb1694/analysis/gui/images/spectrum.png")
photoSpectrum = photo.subsample(3, 3)


wf_btn = Button(master, text="Waveform Browser", image=photoimage, command=Browser).grid(row=0,column=0)
wf_lb = Label(master, text="Waveform Browser").grid(row=1, column=0)

wf_btn = Button(master, text="Spectrum Viewer", image=photoSpectrum, command=lambda: spectrumViewer(master)).grid(row=0,column=1)
wf_lb = Label(master, text="Spectrum Viewer").grid(row=1, column=1)


wf_btn = Button(master, text="Change Daq Data Directory",  command=changeDaqDirectory).grid(row=2,column=0)
wf_btn = Button(master, text="Change Raw Data Directory",  command=changeRawDirectory).grid(row=3,column=0)
wf_btn = Button(master, text="Change Dsp Data Directory",  command=changeDspDirectory).grid(row=4,column=0)


master.mainloop()
