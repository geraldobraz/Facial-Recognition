from tkinter import *
import os
import cv2
import sys
from PIL import Image, ImageTk
import numpy

from TelaCadastro import TelaCadastro
from TelaEntrar import TelaEntrar
def Entrar():
    print("Entrar")
    telaEntrar = TelaEntrar()
    telaEntrar.show()
def Cadastrar():
    print("Cadastrar")
    telaCadastro = TelaCadastro()
    telaCadastro.show()

class TelaOpcoes():
    print("Tela Opcoes")
    def __init__(self):
        self.telaOpcoes = Tk()
        self.telaOpcoes.title('Tela de Opções')
        self.telaOpcoes.geometry('250x300')

    def show(self):

        entrarButton = Button(self.telaOpcoes, height=1, font="Arial 16 normal",text="   Entrar   ",command = Entrar)
        cadastrarButton = Button(self.telaOpcoes, height=1, font="Arial 16 normal",text="Cadastrar",command= Cadastrar)
        label = Label(self.telaOpcoes,font="Arial 18 normal", text="Controle de Acesso")
        label.grid(row=1, column=0, sticky=W)
        entrarButton.grid(row=2, column=0, sticky=W)
        cadastrarButton.grid(row=3, column=0, sticky=W)
        self.telaOpcoes.mainloop()


