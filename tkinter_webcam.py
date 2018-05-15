from tkinter import *
import os
import cv2
import sys
# from PIL import Image, ImageTk
import numpy

cancel = False

def prompt_ok():
    global cancel, cameraButton, button1, button2
    cancel = True

    # FIXME:
    '''
    Estava mais acostumado com o comando GRID para posicionar os componentes.
    Ver isso!
    '''

    cameraButton.place_forget()
    button1 = Button(mainWindow, text="Good Image!", command=saveAndExit)
    button2 = Button(mainWindow, text="Try Again", command=resume)
    button1.place(anchor=CENTER, relx=0.2, rely=0.9, width=150, height=50)
    button2.place(anchor=CENTER, relx=0.8, rely=0.9, width=150, height=50)
    button1.focus()

def saveAndExit():
    global prevImg

    if (len(sys.argv) < 2):
        filepath = "imageCap.jpg"
    else:
        filepath = sys.argv[1]

    print ("Output file to: " + filepath)
    prevImg.save(filepath)
    mainWindow.quit()

def resume():
    global button1, button2, cameraButton, mainLabel, cancel

    cancel = False

    button1.place_forget()
    button2.place_forget()

    mainWindow.bind('<Return>', prompt_ok)
    cameraButton.place(bordermode=INSIDE, relx=0.5, rely=0.9, anchor=CENTER, width=300, height=50)
    mainLabel.after(10, show_frame)

def show_frame():
    global cancel, prevImg, button

    _, frame = cap.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

    prevImg = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=prevImg)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    if not cancel:
        lmain.after(10, show_frame)


camIndex = 0

cap = cv2.VideoCapture(camIndex)
capWidth = cap.get(3)
capHeight = cap.get(4)

success, frame = cap.read()

if not success:
    if camIndex == 0:
        print("Error, No webcam found!")
        sys.exit(1)

#  Main Window
mainWindow = Tk()
mainWindow.title("Camera Capture")
mainWindow.geometry('500x300')

# Labels - All Labels
mainLabel = Label(mainWindow, text= "CAMERA CAPTURE")

# Buttons - All Buttons
cameraButton = Button(mainWindow, text="Capture", command=prompt_ok)

# Grids - Configurate the grid of all components
cameraButton.grid(row=1, column=0, sticky=W)
mainLabel.grid(row=0, column=0, sticky=W)

# Focus on camera button
cameraButton.focus()


# show_frame()
mainWindow.mainloop()
