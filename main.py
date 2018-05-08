# Projeto Final da Disciplina de Python
# Professor: Hermano Cabral
# Alunos: Geraldo Braz e Pedro Vitor


# Command Line

import sys
import time
import getpass



cpf_Validacao = False

def AddAluno():
    print("- Adição de um novo Aluno -")
    nomeAluno = input("Informe o Nome do aluno: ")

    # Analisando o Cpf
    while True:
        cpfAluno = input("Informe o CPF do Aluno (Só números): ")

        if (True):

            # client.publish("software/cpf/validacao/Env", cpfAluno)
            time.sleep(0.5)

            if True:  # fixme: Falta validar de o cpf existe no BD, no serv esta tudo ok ja retorna via mqtt se existe ou n

                # Analisando o sexo
                while True:
                # while True and cpf_Validacao:
                    sexoAluno = input("Informe o Sexo:\n  M - Masculino\n  F - Feminino\n>> ")
                    if sexoAluno == "M" or sexoAluno == "m" or sexoAluno == "Masculino" or sexoAluno == "masculino":
                        print("Certo")
                        sexoAluno = "Masc"
                        break

                    if sexoAluno == "F" or sexoAluno == "f" or sexoAluno == "Feminino" or sexoAluno == "feminino":
                        print("Certo")
                        sexoAluno = "Fem"
                        break
                # Analisando a Senha
                aux = True
                while aux:
                    # senhaAluno = input("Digite a senha (4 Dígitos): ")
                    senhaAluno = getpass.getpass("Digite a senha (4 Dígitos): ")
                    if len(senhaAluno) == 4:
                        print("Senha ok")
                        msg = str(nomeAluno)+"%"+str(cpfAluno)+"%"+str(sexoAluno)+"%"+str(senhaAluno) # Message sended in Mqtt protocol
                        # client.publish("software/Add_Aluno",msg)
                        print(msg)
                        aux = False
                    else:
                        aux = True
                break
        else:
            print("Cpf Inválido!")

def Cadastrar():

    while True:
        senha_root = getpass.getpass("Digite a senha: ")
            # input("Digite a senha do adm:\n >>")
        if senha_root == "1234":
            break

    nome_ = input("Digite o nome: ")

    # TODO: Reconhecimento facial
    # TODO: Mandar pro BD





def Entrar():
    # TODO:
    '''
    1. Abrir a camera
    2. Se a precisao for maior do 1 95%
    3. Msg que entrou com sucesso


    '''
    print("Entrar")

while True:

    print("*************************")
    print("> O que deseja fazer?")
    resp = input("1. Entrar na Sala \n2. Cadastrar Novo Usuário\n3. Sair\n>> ")

    # Add Alunos novos
    if resp == "1":
        Entrar()
    # Cadastrar
    if resp == "2":
        Cadastrar()
    # Sair
    if resp == "3":
        sys.exit()

# client.loop_forever()