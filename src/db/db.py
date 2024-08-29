import threading
import os
from utils.validade_cpf import validar_cpf

file_lock = threading.Lock()

class Service():
    def __init__(self):
        self.admin = 'admin.txt'
        self.estudantes = 'estudantes.txt'
        self.periodo = 'periodo.txt'
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

    def sobrescrever(self, arquivo, data):
        arquivo = open(os.path.join(self.path, arquivo), "w")
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
    def __init__(self, service: Service):
        estudantes = service.ler(service.estudantes)
        estudantes = estudantes.split('\n')
        estudantes.pop() # Remove o último elemento que é uma string vazia
        self.alunos_total = len(estudantes)

        self.is_open = service.ler(service.periodo) == '1\n'


        self.turmas = {
            'A': Turma('turma_a.txt', service),
            'B': Turma('turma_b.txt', service),
            'C': Turma('turma_c.txt', service),
            'D': Turma('turma_d.txt', service),
            'E': Turma('turma_e.txt', service),
            'F': Turma('turma_f.txt', service),
            'G': Turma('turma_g.txt', service),
            'H': Turma('turma_h.txt', service)
        }

        # Calcula a quantidade de alunos máxima por turma logo que as classes são criadas

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
        service.sobrescrever('1\n')

    def fechar(self, service: Service):
        self.is_open = False
        service.sobrescrever('0\n')

    def getIsOpen(self):
        return self.is_open
  
    def getMaxStudents(self):
        max_students = {}
        for key in self.turmas:
            max_students[key] = self.turmas[key].max

        return max_students
    
    def getActualStudents(self):
        actualStudents = {}
        for key in self.turmas:
            actualStudents[key] = len(self.turmas[key].alunos)

        return actualStudents
    
    def countStudentsByClass(self, service: Service):
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

    def checar_inscricao(self, cpf):
        for turma in self.turmas:
            if cpf in self.turmas[turma].alunos:
                return turma
        
        return False

class Turma():
    def __init__(self, path, service: Service):
        alunos = service.ler(path).split('\n')
        alunos.pop()

        if (alunos):
            self.alunos = alunos
        else:
            self.alunos = []
        self.path = path
        self.max = None

    # Inscreve aluno em uma turma específica
    def inscrever_aluno(self, cpf, service: Service):
      with file_lock:
        cpf = cpf.replace('.', '').replace('-', '')

        if cpf in self.alunos:
          return False
      
        if len(self.alunos) == self.max:
          return False
      
        service.escrever(self.path, cpf + '\n')
        self.alunos.append(cpf)


