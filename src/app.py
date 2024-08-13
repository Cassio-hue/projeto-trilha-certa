from flask import Flask, render_template

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route("/", methods=['GET', 'POST'])
def aluno_login():
  return render_template('aluno/login.html')

@app.route("/admin", methods=['GET', 'POST'])
def admin():
  return render_template('admin/login.html')

@app.route("/admin/menu", methods=['GET', 'POST'])
def admin_menu():
    return render_template('admin/menu.html')


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)