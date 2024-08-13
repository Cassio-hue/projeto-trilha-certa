from flask import Flask, render_template, request
from db.db import Service

app = Flask(__name__, template_folder='templates', static_folder='static')
service = Service()

@app.route("/")
def hello_world():
  return "<h1>Hello, World!</h1>"

@app.route("/admin", methods=['GET', 'POST'])
def admin():
  return render_template('admin/login.html')

@app.post("/admin/login")
def login():
  login = request.form.get('login')
  senha = request.form.get('password')

  print(service.login_aluno(login))

  if (service.login_aluno(login)):
    return 'aluno logou'

  if service.logar(login, senha):
    return 'não smt'
  else:
    return 'smt'

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)