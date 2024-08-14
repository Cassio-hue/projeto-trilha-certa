import os
import platform

class Service():
    def __init__(self):
        self.admin = 'admin.txt'
        self.estudantes = 'estudantes.txt'

        if platform.system() == 'Linux':
            # LINUX
            self.path = os.getcwd() + '/src/db/'
        else:
            #WINDOWS
            self.path = os.getcwd() + '\\src\\db\\'

    def ler(self, arquivo):
        arquivo = open(self.path + arquivo, "r")
        data = arquivo.read()
        arquivo.close()

        return data

    def escrever(self, arquivo, data):
        arquivo = open(self.path + arquivo, "a")
        arquivo.write(data)
        arquivo.close()

    def logar_admin(self, usr_login, usr_senha):
        data = self.ler(self.admin)

        [login, senha] = data.split(';')

        return (usr_login == login) and (usr_senha == senha)

    def logar_aluno(self, cpf):
        data = self.ler(self.estudantes)

        return cpf in data

    def criar_aluno(self, cpf):
        if (cpf.isnumeric() and cpf.len() != 11):
            return False

        cpf = cpf.replace('.', '').replace('-', '')
        self.escrever(self.estudantes, cpf)

        return True
