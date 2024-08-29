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

def test_matricular_alunos():
  def inscrever_aluno(cpf, turma):
    barreira.wait()
    print("CPF > ", cpf)
    periodo.turmas[turma].inscrever_aluno(cpf, service)

  maximo_alunos_turma = periodo.turmas['A'].max

  args_list = [(f"t{i}", "A") for i in range(1, 9)]
  create_threads(inscrever_aluno, args_list)

  print("TESTANDO CONCORRÊNCIA NA MATRÍCULA DE ALUNOS")
  alunos_turma = periodo.turmas['A'].alunos
  time.sleep(2)
  casos = [
     "Quantidade máxima de alunos igual a quantidade de alunos na turma A",
     "Quantidade de alunos na turma A igual a quantidade de alunos no arquivo turma_a.txt"
  ]
  resultados = []

  if (len(alunos_turma) == maximo_alunos_turma):
    resultados.append("OK")
  else:
    resultados.append("ERRO")
  
  alunos_turma_a = service.ler('turma_a.txt').split('\n')
  alunos_turma_a.pop()
  if (maximo_alunos_turma == len(alunos_turma_a)):
    resultados.append("OK")
  else:
    resultados.append("ERRO")

  for i in range(len(casos)):
    print(f"{resultados[i]} - {casos[i]}")
  
  print()
  print("LIMPAR TURMA A...")
  time.sleep(2)
  service.sobrescrever('turma_a.txt', '')

test_matricular_alunos()