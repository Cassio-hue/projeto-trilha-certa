import random
import time
import threading
from db.db import Service, Periodo

array_cpfs = ["66073557574", "74170732120", "53442778735", "48092251436", "68876028650", "63389475885", "56391926662", "29787687705", "65990504250", "28164671207", "53649177978", "65740526612", "71383358907", "47846944630", "74458525816", "34551415367", "01133858546", "36843387292", "44347913702", "17984853622"]

service = Service()
periodo = Periodo(service=service)

def create_threads(fun, args_list):
  threads = []
  for args in args_list:
      t = threading.Thread(target=fun, args=args)
      threads.append(t)
      t.start()

  for t in threads:
      t.join()

def teste_matricular_alunos():
  NUM_THREADS = 8
  barreira = threading.Barrier(NUM_THREADS)

  time.sleep(1)
  service.sobrescrever('turma_a.txt', '')

  def inscrever_aluno(cpf, turma):
    barreira.wait()
    periodo.turmas[turma].inscrever_aluno(cpf, service)

  # TESTE DE CONCORRÊNCIA NA MATRÍCULA DE ALUNOS
  maximo_alunos_turma = periodo.turmas['A'].max

  args_list = [(f"t{i}", "A") for i in range(1, 9)]
  create_threads(inscrever_aluno, args_list)

  print("TESTANDO CONCORRÊNCIA NA MATRÍCULA DE ALUNOS\n")
  alunos_turma = periodo.turmas['A'].alunos
  time.sleep(2)
  casos = [
     "Quantidade máxima de alunos permitidos é maior ou igual a quantidade de alunos na classe da turma A",
     "Quantidade máxima de alunos permitidos é maior ou igual a quantidade de alunos no arquivo turma_a.txt",
     "Alunos presentes na classe da turma A são os mesmos que estão no arquivo turma_a.txt"
  ]
  resultados = []

  # CASO 0
  if (maximo_alunos_turma >= len(alunos_turma)):
    resultados.append("OK")
  else:
    resultados.append("ERRO")
  
  # CASO 1
  alunos_turma_a = service.ler('turma_a.txt').split('\n')
  alunos_turma_a.pop()
  if (maximo_alunos_turma >= len(alunos_turma_a)):
    resultados.append("OK")
  else:
    resultados.append("ERRO")

  # CASO 2
  if (alunos_turma == alunos_turma_a):
    resultados.append("OK")
  else:
    resultados.append("ERRO")

  # RESULTADOS
  for i in range(len(casos)):
    print(f"{resultados[i]} - {casos[i]}")
  
  time.sleep(1)
  service.sobrescrever('turma_a.txt', '')


def teste_inscrever_alunos():
  NUM_THREADS = 8
  barreira = threading.Barrier(NUM_THREADS)

  time.sleep(1)
  service.sobrescrever('estudantes.txt', '')

  def criar_aluno(thread, cpf):
    barreira.wait()
    service.criar_aluno(cpf)

  
  random_cpfs = random.sample(array_cpfs, 8)

  args_list = [(f"t{i} - {random_cpfs[i-1]}", random_cpfs[i-1]) for i in range(1, 9)]
  create_threads(criar_aluno, args_list)

  print("TESTANDO INSCRIÇÃO DE ALUNOS NO SISTEMA\n")
  casos = [
     "Alunos presentes no arquivo estudantes.txt são os mesmos que estão no array de cpfs",
     "Quantidade de alunos presentes no arquivo estudantes.txt é igual a o tamanho do array de cpfs",
  ]

  alunos = service.ler('estudantes.txt').split('\n')
  alunos.pop()

  # CASO 0
  def verifica_cpfs():
    for cpf in alunos:
      if cpf not in random_cpfs:
        return False
    return True

  if (verifica_cpfs()):
    print("OK - " + casos[0])
  else:
    print("ERRO - " + casos[0])


  # CASO 1
  if (len(alunos) == len(random_cpfs)):
    print("OK - " + casos[1])
  else:
    print("ERRO - " + casos[1])


print()
teste_matricular_alunos()
print()
teste_inscrever_alunos()
print()



