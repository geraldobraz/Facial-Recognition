from tkinter import *
# from tkinter import filedialog
from tkinter.filedialog import *
import os
import cv2
# import sys
# from PIL import Image, ImageTk
import numpy as np
from tkinter import messagebox
import time
from pycpfcnpj import cpfcnpj
import mysql.connector

global detect_frontalface
detect_frontalface = 'C:\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml'
# 'C:\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml'
# '/home/geraldobraz/opencv-3.4.1/data/haarcascades/haarcascade_frontalface_default.xml'
'''
cnx = mysql.connector.connect(user='root', password='senha',
                              host='localhost',
                              database='Facial_DataBase')

add_Usuarios = ("INSERT INTO Usuarios "
               "(NOME, CPF) "
               "VALUES (%s, %s)")

update_senha = ("UPDATE Alunos SET SENHA = %s" 
                "WHERE CPF = %s")

def ProcuraCpf(ValorCpf):
    cursor = cnx.cursor()
    query = ("SELECT CPF FROM Usuarios ")

    cursor.execute(query)

    validador_cpf = False
    for row in cursor:
        if (ValorCpf in row):
            print(row)
            print("Cpf existe e esta no banco")
            validador_cpf = True
        else:
            print(row)
            print("Cpf nao eh esse")

    cursor.close()
    return validador_cpf
'''


def detect_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(detect_frontalface)

    rosto = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5);

    if (len(rosto) == 0):
        return None, None

    # under the assumption that there will be only one face, extract the face area
    (x, y, w, h) = rosto[0]

    # return only the face part of the image
    return gray[y:y + w, x:x + h], rosto[0]


class Finalize():
    def __init__(self, master, cpf, nome):
        # TODO:    Add no BD a imagem pelo cpf que recebeu
        print("Finalize")

        self.nome = nome
        self.cpf = cpf
        '''
        # http://www.mysqltutorial.org/python-mysql-blob/
        # FIXME: Add as fotos no BD
        dados = (self.nome, self.cpf)
        cursor = cnx.cursor()
        cursor.execute(add_Usuarios, dados)
        cnx.commit()
        cursor.close()
        print("Dados Salvos")
        '''


class Choice():
    def __init__(self, master, cpf, nome):
        print("Choice")
        self.nome = nome
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
        finalize = Finalize(root, self.cpf, self.nome)


class TelaWebcam_Save():
    # sampleNum = 0
    idNum = 0
    def __init__(self, master, cpf, nome, sampleNum, qtdeImagens):
        self.Tela = Toplevel(root)
        self.cpf = cpf
        self.nome = nome
        self.sampleNum = 0
        # self.sampleNum = sampleNum
        self.highestValue = sampleNum
        # self.telaWebcam_save.geometry("300x150")
        self.pegarImagem()
        print("SampleNum is " + str(self.sampleNum))
        # self.moveNext()

    def pegarImagem(self):

        self.Tela.destroy()
        # self.telaWebcam_save.destroy()
        # print("First" + str(sampleNum))
        face_cascade = cv2.CascadeClassifier(detect_frontalface)

        cam = cv2.VideoCapture(0)
        while True:
            _, frame = cam.read()
            # cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                self.sampleNum += 1
                self.upload2BD(frame, self.sampleNum)
                # cv2.imwrite("dataSet/User." + str(self.idNum) + "." + str(self.sampleNum) + ".jpg", gray[y:y + h, x:x + w])
                # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.waitKey(100)

            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            elif self.sampleNum > self.highestValue:
            # elif self.sampleNum > self.highestValue + 5:
                break
            cv2.imshow("Face", frame)
            # self.upload2BD(frame, self.sampleNum)
            cv2.waitKey(1)
        cam.release()
        cv2.destroyAllWindows()
        # self.upload2BD(frame, sampleNum)

        # treina a partir das fotos tiradas
        train = Train(self.directory, self.cpf, self.nome)

    def upload2BD(self, aux, num):

        # cria uma pasta a partir do cpf para salvar as fotos da webcam
        self.directory = './Imagens/' + str(self.cpf) + '/'
        try:
            if not os.path.exists(self.directory):
                os.makedirs(self.directory)
            # print("Imagens/"+ self.cpf+".jpg")
            # cv2.imwrite("Imagens/" + str(num) + '_' + str(self.cpf) + ".jpg", aux)
            cv2.imwrite(self.directory + str(num) + '.jpg', aux)
        except OSError:
            print('Error: Creating directory. ' + self.directory)

        # self.telaWebcam_save.quit()
        time.sleep(0.5)
        telaChoice = Choice(root, self.cpf, self.nome)


class Train():
    def __init__(self, files, cpf, nome):
        self.nome = nome
        self.cpf = cpf
        # caminho das imagens para realizar treinamento
        self.faces = []
        self.dir = [str(files) + '/' + i for i in os.listdir(files) if i.endswith(".jpg")]

        # treinamento e salvamento
        self.faces_train = self.prepare_training_data()
        self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.label = [_ for _ in range(1, len(self.faces_train)+1)]
        self.face_recognizer.train(self.faces_train, np.array(self.label))

        # cria a pasta 'training', se não existir
        self.directory = './training/'
        try:
            if not os.path.exists(self.directory):
                os.makedirs(self.directory)
        except OSError:
            print('Error: Creating directory. ' + self.directory)

        self.face_recognizer.save("training/" + str(self.cpf) + ".yml")
        print('FOI')
        telaChoice = Choice(root, self.cpf, self.nome)

    def prepare_training_data(self):
        for self.dir_img in self.dir:
            # não lê arquivos do tipo .yml, caso exista
            # if self.dir_img.endswith(".yml"):
            #     continue

            # lê uma imagem e detecta a face
            self.image = cv2.imread(self.dir_img)
            # cv2.imshow("Training on image...", cv2.resize(self.image, (400, 500)))
            # cv2.waitKey(100)

            # self.face, _ = self.detect_face(self.image)
            self.face, _ = detect_face(self.image)
            cv2.imshow("Face detection", cv2.resize(self.face, (400, 500)))
            cv2.waitKey(100)

            # se a face não for detectada, a imagem será desconsiderada
            if self.face is not None:
                self.faces.append(self.face)

        # caso tire o imshow após o imread, retirar essa parte
        cv2.destroyAllWindows()
        cv2.waitKey(1)
        cv2.destroyAllWindows()

        return self.faces


class TelaCadastro():
    qtdeImagens = 0

    def __init__(self, master):
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
        print(self.nome, self.cpf)
        # if cpfcnpj.validate(self.cpf):
        #     if not ProcuraCpf(self.cpf):
        #         # Salvar os dados no MySQL
        #         # telaWebcam_Save = TelaWebcam_Save(root, self.cpf, self.nome, sampleNum, self.qtdeImagens)
        #         self.facialRecognation()
        #     else:
        #         messagebox.showerror("Erro", "O CPF já foi cadastrado!")
        # else:
        #     messagebox.showerror("Erro", "O CPF inválido!")
        self.facialRecognation()

    def facialRecognation(self):
        self.Tela.destroy()
        sampleNum = 8
        self.telaWebcam_Save = TelaWebcam_Save(root, self.cpf, self.nome, sampleNum, self.qtdeImagens)

        # cria uma pasta a partir do cpf para salvar as fotos da webcam
        # self.directory = './cpfs/'+str(self.cpf)+'/'
        # try:
        #     if not os.path.exists(self.directory):
        #         os.makedirs(self.directory)
        # except OSError:
        #     print('Error: Creating directory. ' + self.directory)

        # ftypes = [('jpg file', "*.jpg")]
        # root.fileName = askopenfilenames(filetypes=ftypes)
        # root.fileName = askdirectory()

        # treina e salva na pasta
        # train = Train(root.fileName, self.cpf, self.nome)


class Entrou():
    def __init__(self, master):
        self.Tela = Toplevel(root)
        self.Tela.title('TOP')
        self.Tela.geometry('300x200')
        Label(self.Tela, text="Parabéns!").grid()


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
        self.imagem_entrar()
        # if cpfcnpj.validate(self.cpf) and ProcuraCpf(self.cpf):
        #     # TODO: Testar validade do cpf
        #     ftypes = [('jpg file', "*.jpg")]
        #     root.fileName = askopenfilenames(filetypes=ftypes)
        #     self.predict(root.fileName)

        #     try:
        #         # x = os.open("s1/1.jpg",os.O_RDONLY)
        #
        #     #     TODO: Open folder
        #     except:
        #     # Erro tela
        #         messagebox.showerror("Erro", "Cpf não está Cadastrado")

        # else:
        #     messagebox.showerror("Erro", "CPF inválido")

    def imagem_entrar(self):
        self.directory = './Entrar/'
        self.diretorio = self.directory + str(self.cpf) + '_entrar.jpg'
        highestValue = 10
        sampleNum = 0
        face_cascade = cv2.CascadeClassifier(detect_frontalface)

        cam = cv2.VideoCapture(0)
        while True:
            _, frame = cam.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                sampleNum += 1
                cv2.waitKey(100)

            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            elif sampleNum > highestValue:
                break
            cv2.imshow("Face", frame)
            cv2.waitKey(1)

        try:
            if not os.path.exists(self.directory):
                os.makedirs(self.directory)
            # cv2.imwrite("Imagens/" + str(num) + '_' + str(self.cpf) + ".jpg", aux)
            # cv2.imwrite(self.directory + str(self.cpf) + '.jpg', aux)
            cv2.imwrite(self.diretorio, frame)
        except OSError:
            print('Error: Creating directory. ' + self.directory)

        self.predict(self.diretorio)
        cam.release()
        cv2.destroyAllWindows()

    def predict(self, im):
        self.img = cv2.imread(im)
        self.imag = self.img.copy()

        self.rost, self.rect = detect_face(self.imag)
        self.model = cv2.face.LBPHFaceRecognizer_create()

        # testar se existe pasta
        # cria a pasta 'training', se não existir
        self.directory = './training/' + str(self.cpf) + '.yml'
        if os.path.exists(self.directory):
            self.model.read(self.directory)
        else:
            print('Não existe esse diretório')

        # Predicts a label and associated confidence (e.g. distance) for a given input image.
        # confidence: the distance to the closest item in the database (0 would be a "perfect match")
        self.labels, self.confidence = self.model.predict(self.rost)

        # print('labels:', self.labels)
        print('confidence:', self.confidence)
        if self.confidence < 10:
            print('Entrada permitida')
            entrar = Entrou(root)
        else:
            print('Entrada negada')
            messagebox.showerror("Erro", "Face não corresponde ao CPF")


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
