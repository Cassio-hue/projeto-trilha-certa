import os
from utils.validade_cpf import validar_cpf

class Service():
    def __init__(self):
        self.admin = 'admin.txt'
        self.estudantes = 'estudantes.txt'
        # self.turma_a = 'turma_a.txt'
        # self.turma_b = 'turma_b.txt'
        # self.turma_c = 'turma_c.txt'
        # self.turma_d = 'turma_d.txt'
        # self.turma_e = 'turma_e.txt'
        # self.turma_f = 'turma_f.txt'
        # self.turma_g = 'turma_g.txt'
        # self.turma_h = 'turma_h.txt'
        self.path = os.path.join(os.getcwd(), 'src', 'db')

        self.total_max_cpfs = 240

    def ler(self, arquivo):
        arquivo = open(os.path.join(self.path, arquivo), "r")
        data = arquivo.read()
        arquivo.close()

        return data

    def escrever(self, arquivo, data):
        arquivo = open(os.path.join(self.path, arquivo), "a")
        arquivo.write(data)
        arquivo.close()

    def logar_admin(self, usr_login, usr_senha):
        data = self.ler(self.admin)

        [login, senha] = data.split(';')

        return (usr_login == login) and (usr_senha == senha)

    def logar_aluno(self, cpf):
        data = self.ler(self.estudantes)
        cpf = cpf.replace('.', '').replace('-', '')

        if validar_cpf(cpf):
          return cpf in data
        
        return False

    def criar_aluno(self, cpf):
        total_max_alunos, _ = self.total_alunos()
        
        cpf = cpf.replace('.', '').replace('-', '')
        if (cpf.isnumeric() and not validar_cpf(cpf)):
            return False

        data = self.ler(self.estudantes).split('\n')
        if cpf in data:
            return False

        if total_max_alunos == self.total_max_cpfs:
            return False
        
        self.escrever(self.estudantes, cpf + '\n')

        return True
    
    def total_alunos(self):
        data = self.ler(self.estudantes)
        data = data.split('\n')
        data.pop()

        return (len(data), self.total_max_cpfs)
    

class Periodo():
    def __init__(self):
        self.alunos_total = 0
        self.is_open = False
        self.turmas = {
            'A': Turma('turma_a.txt'),
            'B': Turma('turma_b.txt'),
            'C': Turma('turma_c.txt'),
            'D': Turma('turma_d.txt'),
            'E': Turma('turma_e.txt'),
            'F': Turma('turma_f.txt'),
            'G': Turma('turma_g.txt'),
            'H': Turma('turma_h.txt')
        }

    def abrir(self, service: Service):
        estudantes = service.ler(service.estudantes)
        estudantes = estudantes.split('\n')
        estudantes.pop() # Remove o último elemento que é uma string vazia
        self.alunos_total = len(estudantes)

        if (self.alunos_total % 8 == 0):
            for turma in self.turmas:
                self.turmas[turma].max = self.alunos_total // 8
        else:
            min = self.alunos_total // 8

            for turma in self.turmas:
                self.turmas[turma].max = min

            resto = self.alunos_total % 8

            for turma in self.turmas:
                if resto == 0:
                    break
                self.turmas[turma].max += 1
                resto -= 1

        self.is_open = True

    def fechar(self):
        self.is_open = False

class Turma():
    def __init__(self, path):
        self.path = path
        self.alunos = []
        self.max = None

    # Inscreve aluno em uma turma específica
    def inscrever_aluno(self, cpf, service: Service):
        cpf = cpf.replace('.', '').replace('-', '')

        if cpf in self.alunos:
            return False
        
        if len(self.alunos) == self.max:
            return False
        
        service.escrever(self.path, cpf + '\n')
        self.alunos.append(cpf)

        print(self.alunos)


