from flask import Flask, render_template, request, redirect, url_for, session, flash
from db.db import Service, Periodo

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

service = Service()
periodo = Periodo(service=service)

def auth_guard():
  if 'role' not in session:
    return False
  return True

def admin_guard():
  if 'role' in session:
    if session['role'] == 'ADMIN':
      return True

  return False

def periodo_guard():
  if periodo.getIsOpen():
    return True

  return False

def check_inscription(cpf):
  cpf = cpf.replace('.', '').replace('-', '')
  return periodo.checar_inscricao(cpf)

def remove_session():
  session.pop('role', None)
  session.pop('cpf_aluno', None)


@app.get("/logout")
def logout():
  remove_session()
  return app.redirect(app.url_for('index'))

@app.route("/periodo-fechado")
def periodo_fechado():
  if (periodo_guard()):
    if (auth_guard()):
      return app.redirect(app.url_for('aluno_menu'))
    return app.redirect(app.url_for('index'))
  
  return render_template('not-found/periodo-fechado.html')

@app.route("/inscricao-realizada/<turma>")
def inscricao_realizada(turma):
  return render_template('inscricao-realizada/inscricao-realizada.html', turma=turma)

@app.route("/", methods=['GET', 'POST'])
def index():
  if (auth_guard()):
    return app.redirect(app.url_for('aluno_menu'))

  if (request.method == 'POST'):
    remove_session()
    cpf = request.form.get('cpf')
    if service.logar_aluno(cpf):
      session['cpf_aluno'] = request.form['cpf']
      session['role'] = 'ALUNO'

      if (not periodo_guard()):
        return app.redirect(app.url_for('periodo_fechado'))
      
      res = check_inscription(cpf)
      if (res):
        return app.redirect(app.url_for('inscricao_realizada', turma=res))
      
      return app.redirect(app.url_for('aluno_menu'))
    flash("CPF inválido ou não cadastrado", "error")

  return render_template('aluno/login.html')

@app.route("/admin", methods=['GET', 'POST'])
def admin():
  if (not admin_guard() and auth_guard()):
    return app.redirect(app.url_for('index'))

  if (request.method == 'POST'):
    remove_session()
    login = request.form.get('login')
    senha = request.form.get('password')
    if service.logar_admin(login, senha):
      session['role'] = 'ADMIN'
      return app.redirect(app.url_for('admin_menu'))
    else:
      flash("Login ou senha incorretos", "error")
      return app.redirect(app.url_for('admin'))
  elif (auth_guard()):
    return app.redirect(app.url_for('admin_menu'))

  return render_template('admin/login.html')


@app.get("/admin/menu")
def admin_menu():
  if not (admin_guard()):
    return app.redirect(app.url_for('index'))
  
  total_alunos, total_max_alunos = service.total_alunos()
  return render_template('admin/menu.html', total_alunos=total_alunos, total_max_alunos=total_max_alunos)

@app.post("/admin/criar-aluno")
def criar_aluno():
    cpf = request.form.get('cpf')
    if service.criar_aluno(cpf):
        return redirect(url_for('admin_menu'))
    else:
        return redirect(url_for('admin_menu'))

@app.post("/admin/abrir-periodo")
def abrir_periodo():
    periodo.abrir(service)
    flash("Período aberto com sucesso", "success")
    return redirect(url_for('admin_menu'))

@app.route("/aluno_menu", methods=['GET', 'POST'])
def aluno_menu():
  if not (auth_guard()):
    return app.redirect(app.url_for('index'))
  
  if (not periodo_guard()):
    remove_session()
    return app.redirect(app.url_for('index'))
  
  max_students = periodo.getMaxStudents()
  actual_students = periodo.getActualStudents()
  
  # if (request.method == 'POST'):
      # cpf = session['cpf_aluno']
      # periodo.turmas[turma].inscrever_aluno(cpf, service)

  return render_template('aluno/menu.html', max_students=max_students, actual_students=actual_students)

@app.route("/aluno/matricular/<turma>", methods=['GET', 'POST'])
def matricular(turma):
    if (periodo.getIsOpen() and not turma):
        max_students = periodo.getMaxStudents()
        actual_students = periodo.getActualStudents()
        return render_template('aluno/menu.html', max_students=max_students, actual_students=actual_students)

    cpf = session['cpf_aluno']
    periodo.turmas[turma].inscrever_aluno(cpf, service)

    remove_session()

    return redirect(url_for('index'))

@app.route("/admin/relatorio", methods=['GET', 'POST'])
def relatorio():
    estudantes = periodo.estudantesPorTurma()

    return render_template('admin/relatorio.html', estudantes=estudantes)

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)