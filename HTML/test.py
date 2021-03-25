from flask import Flask, redirect, url_for, render_template

app = Flask(__name__, static_url_path='/static')

@app.route("/")
def home():
    return render_template("Hitta_resa.html")

@app.route("/gillar")
def gillar():
    return render_template("gillar.html")

@app.route("/filter")
def filter():
    return render_template("filter.html")

if __name__ == '__main__':
    app.defug = True
    app.run(host = '127.0.0.1', port = 5000)