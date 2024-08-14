from flask import Flask, render_template, request, redirect, url_for
from db.db import Service, Periodo

app = Flask(__name__, template_folder='templates', static_folder='static')
service = Service()
periodo = Periodo()


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
  if (request.method == 'POST'):
    login = request.form.get('login')
    senha = request.form.get('password')
    if service.logar_admin(login, senha):
      return app.redirect(app.url_for('admin_menu'), 200)
    else:
      return app.redirect(app.url_for('admin_menu'), 500)
      return render_template('admin/login.html', error='Login ou senha inválidos')

  return render_template('admin/login.html')

#Tela e rotas do menu do admin

@app.get("/admin/menu")
def admin_menu():
  return render_template('admin/menu.html')

@app.post("/admin/criar-aluno")
def criar_aluno():
    cpf = request.form.get('cpf')
    if service.criar_aluno(cpf):
        return redirect(url_for('admin_menu'))
        return render_template('admin/menu.html', success='Aluno criado com sucesso')
    else:
        return render_template('admin/menu.html', error='Erro ao criar aluno')

@app.post("/admin/abrir-periodo")
def abrir_periodo():
    periodo.abrir(service)
    return render_template('admin/menu.html')
  


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)