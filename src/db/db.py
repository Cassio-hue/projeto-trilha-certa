import os

class Service():
  def __init__(self):
    self.admin = 'admin.txt'
    self.estudantes = 'estudantes.txt'
    self.path = os.path.join(os.getcwd(), 'src', 'db')

  def logar(self, usr_login, usr_senha):
    arquivo = open(os.path.join(self.path, self.admin), "r")
    data = arquivo.read()
    arquivo.close()

    [login, senha] = data.split(';')

    return usr_login == login and usr_senha == senha


  def criar_aluno(self, cpf):
    arquivo = open(os.path.join(self.path, self.estudantes), "a")
    arquivo.write(cpf + '\n')
    arquivo.close()

  def login_aluno(self, cpf):
    print(self.path)
    arquivo = open(os.path.join(self.path, self.estudantes), "r")
    data = arquivo.read()
    arquivo.close()


    data = data.split('\n')

    return cpf in data