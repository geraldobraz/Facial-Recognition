from tkinter import *
import os
import cv2
import sys
from PIL import Image, ImageTk
import numpy

'''class TelaEntrar():
    def __init__(self):
        self.cancel = True
        self.camIndex = 0
        self.cap = cv2.VideoCapture(self.camIndex)
        self.button

    def show(self):
        entrouLabel = Label(self.telaEntrar,text = "ENTROU")
        entrouLabel.grid()
        self.telaEntrar.mainloop()
        self.telaEntrar = Tk()
        self.telaEntrar.title('Tela de Inicio')
        self.telaEntrar.geometry('250x300')
        self.telaEntrar.resizable(width=False, height=False)
        self.telaEntrar.bind('<Escape>', lambda e: self.telaEntrar.quit())
        self.lmain = Label(self.telaEntrar, compound=CENTER, anchor=CENTER, relief=RAISED)
        self.button = Button(self.telaEntrar, text="Tirar foto", command=self.prompt_ok())
        self.lmain.pack()
        self.button.place(bordermode=INSIDE, relx=0.5, rely=0.9, anchor=CENTER, width=300, height=50)
        self.button.focus()

    def prompt_ok(self, event = 0):
        self.button.place_forget()
        self.button1 = Button(self.telaEntrar, text="Good Image!", command=self.permitir())
        self.button2 = Button(self.telaEntrar, text="Try Again", command=self.resume())
        self.button1.place(anchor=CENTER, relx=0.2, rely=0.9, width=150, height=50)
        self.button2.place(anchor=CENTER, relx=0.8, rely=0.9, width=150, height=50)
        self.button1.focus()

    def permitir(self, event = 0):
        if len(sys.argv) < 2:
            self.filepath = "imageCap.jpg"
        else:
            self.filepath = sys.argv[1]

        print("Output file to: " + self.filepath)
        self.prevImg.save(self.filepath)
        self.telaEntrar.quit()

    def resume(self, event = 0):
        self.cancel = False

        self.button1.place_forget()
        self.button2.place_forget()

        self.telaEntrar.bind('<Return>', self.prompt_ok())
        self.button.place(bordermode=INSIDE, relx=0.5, rely=0.9, anchor=CENTER, width=300, height=50)
        self.lmain.after(10, self.show_frame())

    def show_frame(self):
        self.sucess, self.frame = self.cap.read()
        if not self.success:
            if self.camIndex == 0:
                print("Erro, webcam não encontrada!")
                sys.exit(1)

        self.cv2image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGBA)

        self.prevImg = Image.fromarray(self.cv2image)
        self.imgtk = ImageTk.PhotoImage(image=self.prevImg)
        self.lmain.imgtk = self.imgtk
        self.lmain.configure(image=self.imgtk)
        if not self.cancel:
            self.lmain.after(10, self.show_frame())'''



def prompt_ok(event = 0):
    global cancel, button, button1, button2, mainWindow
    cancel = True

    button.place_forget()
    button1 = Button(mainWindow, text="Good Image!", command=saveAndExit)
    button2 = Button(mainWindow, text="Try Again", command=resume)
    button1.place(anchor=CENTER, relx=0.2, rely=0.9, width=150, height=50)
    button2.place(anchor=CENTER, relx=0.8, rely=0.9, width=150, height=50)
    button1.focus()

def saveAndExit(event = 0):
    global prevImg, mainWindow

    if (len(sys.argv) < 2):
        filepath = "imageCap.jpg"
    else:
        filepath = sys.argv[1]

    print ("Output file to: " + filepath)
    prevImg.save(filepath)
    mainWindow.quit()


def resume(event = 0):
    global button1, button2, button, lmain, cancel, mainWindow

    cancel = False

    button1.place_forget()
    button2.place_forget()

    mainWindow.bind('<Return>', prompt_ok)
    button.place(bordermode=INSIDE, relx=0.5, rely=0.9, anchor=CENTER, width=300, height=50)
    lmain.after(10, show_frame)

def show_frame():
    global cancel, prevImg, button, cap, lmain

    _, frame = cap.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

    prevImg = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=prevImg)
    lmain.imgtk = imgtk
    lmain.config(image=imgtk)
    if not cancel:
        lmain.after(10, show_frame())

def start():
    global cancel, prevImg, button, lmain, cap, mainWindow
    cancel = False
    camIndex = 0

    cap = cv2.VideoCapture(camIndex)

    success, frame = cap.read()
    if not success:
        if camIndex == 0:
            print("Error, No webcam found!")
            sys.exit(1)

    # mainWindow = Tk(screenName="Camera Capture")
    mainWindow = Toplevel()
    mainWindow.title("Camera Capture")
    mainWindow.resizable(width=False, height=False)
    mainWindow.bind('<Escape>', lambda e: mainWindow.quit())
    lmain = Label(mainWindow, compound=CENTER, anchor=CENTER, relief=RAISED)
    button = Button(mainWindow, text="Capture", command=prompt_ok)

    lmain.pack()
    button.place(bordermode=INSIDE, relx=0.5, rely=0.9, anchor=CENTER, width=300, height=50)
    button.focus()

    show_frame()
    mainWindow.mainloop()
