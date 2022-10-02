from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import filedialog
import sys
import os
import customtkinter

# adding Folder_2/subfolder to the system path
dir = os.getcwd()
sys.path.insert(0, dir + '/scripts')
sys.path.insert(0, dir + '/scripts/waveformBrowser')

from changeDirectory import *
from spectrum import spectrumViewer
from wfBrowse import browseClass

master = customtkinter.CTk()
master.configure(bg='gray20')
master.title("Pygama Analysis GUI")
ico = Image.open('images/gamma.png')
photo = ImageTk.PhotoImage(ico)
master.wm_iconphoto(False, photo)
master.geometry("1000x800")

directFrame = customtkinter.CTkFrame(master, width=250, height=800, fg_color='gray')
directFrame.place(x=0,y=0)
appFrame = customtkinter.CTkFrame(master, width=650, height=700, fg_color='gray')
appFrame.place(x=300, y=30)

dir = os.getcwd()

photo = PhotoImage(file = dir + "/images/wfBrowser.png")
photoimage = photo.subsample(3, 3)

photo = PhotoImage(file = dir + "/images/spectrum.png")
photoSpectrum = photo.subsample(3, 3)


appLbl = customtkinter.CTkLabel(text="Applications", text_font=('Times', 12), bg_color='gray')
appLbl.place(x=320, y=40)

wf_btn = customtkinter.CTkButton(appFrame, text="Waveform Browser", image=photoimage, command=lambda: browseClass(master),
 width=50, height=85, fg_color='white', text_color='black', compound='right', text_font=('Times', 12))
wf_btn.place(x=10,y=50)

spec_btn = customtkinter.CTkButton(appFrame, text="Spectrum Viewer", image=photoSpectrum,
width=50, height=50, fg_color='white', text_color='black', command=lambda: spectrumViewer(master), compound='right',
 text_font=('Times', 12))
spec_btn.place(x=250,y=50)

dirLbl = customtkinter.CTkLabel(text="File Directories", text_font=('Times', 12), bg_color='gray')
dirLbl.place(x=20, y=10)

daq_btn = customtkinter.CTkButton(directFrame, text="Change Daq Data Directory",  command=changeDaqDirectory,
width=50, height=50, fg_color='white', text_color='black', text_font=('Times', 12))
daq_btn.place(x=20, y=50)
raw_btn = customtkinter.CTkButton(directFrame, text="Change Raw Data Directory",  command=changeRawDirectory,
width=50, height=50, fg_color='white', text_color='black', text_font=('Times', 12))
raw_btn.place(x=20, y=150)
dsp_btn = customtkinter.CTkButton(directFrame, text="Change Dsp Data Directory",  command=changeDspDirectory,
width=50, height=50, fg_color='white', text_color='black', text_font=('Times', 12))
dsp_btn.place(x=20, y=250)


master.mainloop()
