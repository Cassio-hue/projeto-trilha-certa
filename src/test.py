import time
import threading
from db.db import Service, Periodo

NUM_THREADS = 8
barreira = threading.Barrier(NUM_THREADS)

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
  time.sleep(2)
  service.sobrescrever('turma_a.txt', '')

  def inscrever_aluno(cpf, turma):
    barreira.wait()
    periodo.turmas[turma].inscrever_aluno(cpf, service)

  # TESTE DE CONCORRÊNCIA NA MATRÍCULA DE ALUNOS
  maximo_alunos_turma = periodo.turmas['A'].max

  args_list = [(f"t{i}", "A") for i in range(1, 9)]
  create_threads(inscrever_aluno, args_list)

  print("TESTANDO CONCORRÊNCIA NA MATRÍCULA DE ALUNOS")
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
  
  print()
  print("LIMPAR TURMA A...")
  time.sleep(2)
  service.sobrescrever('turma_a.txt', '')

teste_matricular_alunos()