from flask import Flask, render_template, request
from db.db import Service

app = Flask(__name__, template_folder='templates', static_folder='static')
service = Service()

# Tela e rotas do login do aluno

@app.route("/", methods=['GET', 'POST'])
def aluno_login():
  return render_template('aluno/login.html')

@app.post("/aluno/login")
def logar_aluno():
    cpf = request.form.get('cpf')
    if service.logar_aluno(cpf):
        return 'aluno logado'
    else:
        return render_template('aluno/login.html', error='CPF não cadastrado')

# Tela e rotas do login do admin

@app.route("/admin", methods=['GET', 'POST'])
def admin():
  return render_template('admin/login.html')

@app.post("/admin/login")
def login():
  login = request.form.get('login')
  senha = request.form.get('password')

  if service.logar_admin(login, senha):
    return render_template('admin/menu.html')
  else:
    return render_template('admin/login.html', error='Login ou senha inválidos')
  
#Tela e rotas do menu do admin

@app.route("/admin/menu", methods=['GET', 'POST'])
def admin_menu():
    return render_template('admin/menu.html')

@app.post("/admin/criar_aluno")
def criar_aluno():
  cpf = request.form.get('cpf')
  if service.criar_aluno(cpf):
    return render_template('admin/menu.html', success='Aluno criado com sucesso')
  else:
    return render_template('admin/menu.html', error='Erro ao criar aluno')
  


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)