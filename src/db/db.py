import os

class Service():
    def __init__(self):
        self.admin = 'admin.txt'
        self.estudantes = 'estudantes.txt'
        self.turma_a = 'turma_a.txt'
        self.turma_b = 'turma_b.txt'
        self.turma_c = 'turma_c.txt'
        self.turma_d = 'turma_d.txt'
        self.turma_e = 'turma_e.txt'
        self.turma_f = 'turma_f.txt'
        self.turma_g = 'turma_g.txt'
        self.turma_h = 'turma_h.txt'
        self.path = os.path.join(os.getcwd(), 'src', 'db')

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

        return cpf in data

    def criar_aluno(self, cpf):
        cpf = cpf.replace('.', '').replace('-', '')
        if (cpf.isnumeric() and len(cpf) != 11):
            return False

        self.escrever(self.estudantes, cpf + '\n')

        return True
    

class Periodo():
    def __init__(self):
        self.alunos_total = 0
        self.is_open = False
        self.turmas = {
            'A': Turma(),
            'B': Turma(),
            'C': Turma(),
            'D': Turma(),
            'E': Turma(),
            'F': Turma(),
            'G': Turma(),
            'H': Turma()
        }

    def abrir(self, service: Service):
        estudantes = service.ler(service.estudantes)
        estudantes = estudantes.split('\n')
        estudantes.pop() # Remove o último elemento que é uma string vazia
        self.alunos_total = len(estudantes)
        print(estudantes)

        print(self.alunos_total)
        if (self.alunos_total % 8 == 0):
            for turma in self.turmas:
                self.turmas[turma].max = self.alunos_total // 8
        else:
            min = self.alunos_total // 8
            print('valor min turmas ' + str(min))

            for turma in self.turmas:
                self.turmas[turma].max = min

            resto = self.alunos_total % 8
            print('valor resto ' + str(resto))

            for turma in self.turmas:
                if resto == 0:
                    break
                self.turmas[turma].max += 1
                resto -= 1

        for turma in self.turmas:
          print(f'Turma {turma}: {self.turmas[turma].max}')

        self.is_open = True

    def fechar(self):
        self.is_open = False

    def calcular_total(self):
        total = 0

        for turma in self.turmas:
            total += turma.total

        return total

class Turma():
    def __init__(self):
        self.total = 0
        self.max = None

    def inscrever_aluno(self, cpf,  turma, service: Service):
        self.total += 1
