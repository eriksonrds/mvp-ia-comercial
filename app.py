from flask import Flask, render_template, send_file, send_from_directory, request
import subprocess
import os
import sys

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/gerar", methods=["POST"])
def gerar():
    try:
        subprocess.run([sys.executable, "main.py"], check=True)
        return "", 200
    except subprocess.CalledProcessError as e:
        return f"Erro ao gerar relatório: {str(e)}", 500
    except Exception as e:
        return f"Erro inesperado: {str(e)}", 500

@app.route("/report")
def mostrar_dashboard():
    return send_file("report/index.html")

# ✅ Adicione esta rota para servir os arquivos da pasta assets
@app.route("/assets/<path:filename>")
def assets(filename):
    return send_from_directory("report/assets", filename)

if __name__ == "__main__":
    app.run(debug=True)
