from flask import Flask, render_template

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route("/")
def hello_world():
    return "<h1>Hello, World!</h1>"

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    return render_template('admin/login.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)