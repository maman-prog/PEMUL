from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", nama=None)


@app.route("/proses", methods=["GET", "POST"])
def proses():
    nama = None
    if request.method == "POST":
        nama = request.form.get("nama", "").strip()
    return render_template("index.html", nama=nama)


