import os
import cv2
import sys
from PIL import Image, ImageTk
import numpy
from tkinter import *

face_cascade = cv2.CascadeClassifier('/home/geraldobraz/opencv-3.4.1/data/haarcascades/haarcascade_frontalface_default.xml')
cancel = False

class TelaWebcam():


    def prompt_ok(self):
        global cancel, mainButton, saveButton, tryAgainButton
        cancel = True

        self.mainButton.place_forget()
        saveButton = Button(self.telaWebcam, text="Save", command = self.saveAndExit)
        tryAgainButton = Button(self.telaWebcam, text="Try Again",  command= self.resume)
        saveButton.place(anchor=CENTER, relx=0.2, rely=0.9, width=150, height=50)
        tryAgainButton.place(anchor=CENTER, relx=0.8, rely=0.9, width=150, height=50)
        saveButton.focus()

    def saveAndExit(self):
        print("Fazer algo")
        #         TODO: Salvar
        global prevImg

        if (len(sys.argv) < 2):
            filepath = "imageCap.jpg"
        else:
            filepath = sys.argv[1]

        print("Output file to: " + filepath)
        prevImg.save(filepath)
        self.telaWebcam.quit()

    def resume(self):
        global saveButton, tryAgainButton,cancel
        cancel = False
        saveButton.place_forget()
        tryAgainButton.place_forget()

        self.mainButton.place(bordermode=INSIDE, relx=0.5, rely=0.9, anchor=CENTER, width=300, height=50)
        self.mainLabel.after(10,self.show_frame)

    def __init__(self):

        # Procurando a Webcam
        camIndex = 0
        self.cap = cv2.VideoCapture(camIndex)
        capWidth = self.cap.get(3)
        capHeight = self.cap.get(4)
        success, frame = self.cap.read()
        if not success:
            if camIndex == 0:
                print("Error, No webcam found!")
                sys.exit(1)

        self.telaWebcam = Tk()
        self.telaWebcam.title('Tela da Webcam')
        # self.telaWebcam.resizable(width=False, height=False)
        self.telaWebcam.geometry('500x500')

        self.mainLabel = Label(self.telaWebcam, compound=CENTER, anchor=CENTER, relief=RAISED)
        self.mainButton = Button(self.telaWebcam, text="Capture", command=self.prompt_ok)

        # self.show_frame()

    def show_frame(self):
        global cancel, prevImg

        _, frame = self.cap.read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        gray = cv2.cvtColor(cv2image, cv2.COLOR_RGB2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2image = cv2.rectangle(cv2image, (x, y), (x + w, y + h), (100, 200, 143), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = cv2image[y:y + h, x:x + w]
        prevImg = Image.fromarray(cv2image) # Linha do Erro!
        # prevImg = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=prevImg)
        self.mainLabel.imgtk = imgtk
        self.mainLabel.configure(image=imgtk)

        if not cancel:
            self.mainLabel.after(10, self.show_frame)

    def show(self):
        self.mainLabel.grid()
        self.mainButton.grid()
        self.mainButton.place(bordermode=INSIDE, relx=0.5, rely=0.9, anchor=CENTER, width=300, height=50)
        self.mainButton.focus()
        self.show_frame()
        self.telaWebcam.mainloop()
        cv2.destroyAllWindows()