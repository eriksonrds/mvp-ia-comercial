from flask import Flask, render_template, send_file, send_from_directory, request
import subprocess
import sys
from pathlib import Path

# Define caminhos base
BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "report"
ASSETS_DIR = REPORT_DIR / "assets"

app = Flask(__name__)


@app.route("/")
def index() -> str:
    """
    Página principal do frontend.

    Returns:
        str: HTML da tela inicial com botão de geração.
    """
    return render_template("index.html")


@app.route("/gerar", methods=["POST"])
def gerar() -> tuple[str, int]:
    """
    Executa o pipeline principal ao clicar no botão "Gerar".

    Returns:
        tuple[str, int]: Resposta HTTP com status 200 ou erro 500.
    """
    try:
        subprocess.run(
            [sys.executable, "main.py"],
            check=True,
            cwd=BASE_DIR
        )
        return "", 200
    except subprocess.CalledProcessError as e:
        return f"❌ Erro ao gerar relatório: {str(e)}", 500
    except Exception as e:
        return f"❌ Erro inesperado: {str(e)}", 500


@app.route("/report")
def mostrar_dashboard():
    """
    Exibe o dashboard HTML gerado após execução do pipeline.

    Returns:
        Response: Arquivo HTML renderizado.
    """
    return send_file(REPORT_DIR / "index.html")


@app.route("/assets/<path:filename>")
def assets(filename: str):
    """
    Serve os arquivos estáticos do dashboard (imagens, CSS).

    Args:
        filename (str): Caminho do arquivo dentro da pasta assets.

    Returns:
        Response: Arquivo solicitado (imagem, CSS, etc).
    """
    return send_from_directory(ASSETS_DIR, filename)


if __name__ == "__main__":
    app.run(debug=True)
