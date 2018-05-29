from tkinter import *
import os
import cv2
import sys
from PIL import Image, ImageTk
import numpy
import mysql.connector

from TelaWebcam import TelaWebcam

'''
>> Configuracao do BD
cnx = mysql.connector.connect(user='root', password='senha',
                              host='localhost',
                              database='Facial_Recognition')

'''


class TelaCadastro():
    def __init__(self):
        self.telaCadastro = Tk()
        self.telaCadastro.title('Tela de Cadastro')
        self.telaCadastro.geometry('300x200')


    def salvarDados(self):
        print("Salvando...")
        # TODO: openCV
        nome = e1.get()
        print(nome)
        self.telaWebcam = TelaWebcam()
        self.telaWebcam.show()

    def show(self):
        Label(self.telaCadastro, text="Nome:").grid(row=0, sticky=E)
        # Nome
        global e1
        e1 = Entry(self.telaCadastro)
        e1.grid(row=0, column=1)
        e1.focus_set()
        Button(self.telaCadastro, text='Adicionar',command = self.salvarDados).grid(row=7, column=1, sticky=W, pady=4)
        self.telaCadastro.mainloop()
        # Abrir uma tela para o openCV e salvar os dados
        # --
        # Salvar no Banco de Dados MySQL
        # --