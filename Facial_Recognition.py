from tkinter import *
# from tkinter import filedialog
from tkinter.filedialog import *
import os
import cv2
# import sys
# from PIL import Image, ImageTk
# import numpy
from tkinter import messagebox
import time

class Finalize():
    def __init__(self, master, cpf):
    #TODO:    Add no BD a imagem pelo cpf que recebeu
        print("Finalize")

class Choice():
    def __init__(self,master,cpf):
        print("Choice")
        self.cpf = cpf
        self.Tela = Toplevel(root)
        self.Tela.geometry("350x150")
        self.Tela.title("Tela Selecionar")
        Button(self.Tela, height=1, font="Arial 16 normal", text="   Menu   ",
                              command=self.Finalizar).grid(row=3, column=0, sticky=W)
        Button(self.Tela, height=1, font="Arial 16 normal", text="Cadastrar Novamente",
                                 command=self.Cadastrar).grid(row=2, column=0, sticky=W)
        Label(self.Tela, font="Arial 18 normal", text="Selecione o que deseja fazer: ").grid(row=1, column=0, sticky=W)


    def Cadastrar(self):
        print("Cadastrar")
        self.Tela.destroy()
        telaCadastro = TelaCadastro(root)

    def Finalizar(self):
        print("Finalizar")
        self.Tela.destroy()
        finalize = Finalize(root, self.cpf)

class TelaWebcam_Save():
    sampleNum = 0
    idNum = 0
    def __init__(self, master, cpf, sampleNum,qtdeImagens):
        self.Tela = Toplevel(root)
        self.cpf = cpf
        self.sampleNum = sampleNum
        # self.highestValue = sampleNum
        # self.telaWebcam_save.geometry("300x150")
        self.pegarImagem()
        print("SampleNum is " + str(self.sampleNum))
        # self.moveNext()

    def pegarImagem(self):
        self.Tela.destroy()
        # self.telaWebcam_save.destroy()
        sampleNum = self.sampleNum
        print("First" + str(sampleNum))
        highestValue = sampleNum
        face_cascade = cv2.CascadeClassifier(
            '/home/geraldobraz/opencv-3.4.1/data/haarcascades/haarcascade_frontalface_default.xml')
        cam = cv2.VideoCapture(0)
        while True:
            _, frame = cam.read()


            # cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                sampleNum += 1
                cv2.imwrite("dataSet/User." + str(self.idNum) + "." + str(self.sampleNum) + ".jpg", gray[y:y + h, x:x + w])
                # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.waitKey(100)
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            elif sampleNum > highestValue + 5:
                break
            cv2.imshow("Face", frame)
            cv2.waitKey(1)
        cam.release()
        cv2.destroyAllWindows()
        self.upload2BD(frame)

    def upload2BD(self, aux):
        print("Imagens/"+ self.cpf+".jpg")
        cv2.imwrite("Imagens/"+ self.cpf+".jpg", aux)
        # self.telaWebcam_save.quit()
        time.sleep(0.5)
        telaChoice = Choice(root, self.cpf)

class Train():
    def __init__(self,files):
        self.dir = files
        # subject_images_names = os.listdir(subject_dir_path)
        # TODO: chamar a tela choice
class TelaCadastro():
    qtdeImagens = 0
    def __init__(self,master):
        self.Tela = Toplevel(root)
        self.Tela.title('Tela de Cadastro')
        self.Tela.geometry('300x200')
        Label(self.Tela, text="Nome:").grid(row=0, sticky=E)
        Label(self.Tela, text="cpf:").grid(row=1, sticky=E)
        # Nome
        global e1
        e1 = Entry(self.Tela)
        e1.grid(row=0, column=1)
        # CPF
        global e2
        e2 = Entry(self.Tela)
        e2.grid(row=1, column=1)
        e1.focus_set()
        Button(self.Tela, text='Adicionar', command=self.salvarDados).grid(row=7, column=1, sticky=W, pady=4)

    def salvarDados(self):
        print("Salvando...")
        # TODO: openCV
        self.nome = str(e1.get())
        self.cpf = str(e2.get())
        print(self.nome,self.cpf)
        # Salvar os dados no MySQL
        # telaWebcam_save = TelaWebcam_Save(self.telaCadastro, self.cpf)
        self.facialRecognation()

    def facialRecognation(self):
        self.Tela.destroy()
        sampleNum = 0
        # self.telaWebcam_Save = TelaWebcam_Save(root,self.cpf,sampleNum,self.qtdeImagens)
        lista = []
        ftypes = [('jpg file', "*.jpg")]
        root.fileName = askopenfilenames(filetypes=ftypes)
        print(root.fileName)
        for i in (root.fileName):
            print(i)
        train = Train(root.fileName)

class TelaEntrar():
    def __init__(self,master):
        self.Tela = Toplevel(root)

        self.Tela.title('Tela de Inicio')
        self.Tela.geometry('300x200')
        Label(self.Tela, text="Digite o CPF :").grid(row=0, sticky=E)
        Label(self.Tela, text="CPF:").grid(row=3, sticky=E)

        # CPF
        global e3
        e3 = Entry(self.Tela)
        e3.grid(row=3, column=1)
        e3.focus_set()
        Button(self.Tela, text='Entrar', command=self.Entrar).grid(row=7, column=1, sticky=W, pady=4)

    def Entrar(self):
        print("Entrou")
        self.cpf = e3.get()
        print(e3.get())
        if True:
            # TODO: Testar validade do cpf
            try:
                 x = os.open("Imagens/101/090.jpg",os.O_RDONLY)

            #     TODO: Open folder
            except:
            # Erro tela
                messagebox.showerror("Erro", "Cpf não está Cadastrado")

        else:
            messagebox.showerror("Erro", "Dados Inválidos")

class TelaOpcoes():
    print("Tela Opcoes")

    def __init__(self,master):
        # self.telaOpcoes = Tk()
        root.geometry('250x300')
        root.title('Tela de Opções')
        entrarButton = Button(root, height=1, font="Arial 16 normal", text="   Entrar   ",
                              command=self.Entrar)
        cadastrarButton = Button(root, height=1, font="Arial 16 normal", text="Cadastrar",
                                 command=self.Cadastrar)
        label = Label(root, font="Arial 18 normal", text="Controle de Acesso")
        label.grid(row=1, column=0, sticky=W)
        entrarButton.grid(row=2, column=0, sticky=W)
        cadastrarButton.grid(row=3, column=0, sticky=W)

    def Entrar(self):
        print("Entrar")
        telaEntrar = TelaEntrar(root)
    def Cadastrar(self):
        print("Cadastrar")
        telaCadastro = TelaCadastro(root)


if __name__ == '__main__':
    root = Tk()
    telaOpcoes = TelaOpcoes(root)
    root.mainloop()