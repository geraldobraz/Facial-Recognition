from tkinter import *
import os
import cv2
import sys
from PIL import Image, ImageTk
import numpy

class TelaEntrar():
    def __init__(self):
        self.telaEntrar = Tk()
        self.telaEntrar.title('Tela de Inicio')
        self.telaEntrar.geometry('250x300')

    def show(self):
        entrouLabel = Label(self.telaEntrar,text = "ENTROU")
        entrouLabel.grid()
        self.telaEntrar.mainloop()