from flask import Flask, render_template, send_file, send_from_directory, jsonify
from pathlib import Path
import pandas as pd

# Define caminhos base
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "report"
ASSETS_DIR = REPORT_DIR / "assets"

app = Flask(
    __name__,
    static_folder="app/static",       # Ajuste conforme seu projeto
    template_folder="app/templates"
)

@app.route("/")
def index():
    """
    Página principal do AI Córtex.
    """
    return render_template("index.html", gerando=False)

@app.route("/dados")
def dados():
    """
    Retorna os dados processados a partir do CSV para os gráficos do dashboard.
    """
    df = pd.read_csv(DATA_DIR / "interacoes_clusterizadas.csv")

    # Gráfico de barras: leads por status
    barras = df["status"].value_counts().reset_index()
    barras.columns = ["status", "quantidade"]
    barras = barras.to_dict(orient="records")

    # Gráfico de clusters: x, y por cluster_kmeans
    clusters = df.groupby("cluster_kmeans")[["x", "y"]].apply(lambda g: g.values.tolist()).to_dict()

    return jsonify({
        "barras": barras,
        "clusters": clusters
    })

@app.route("/report")
def mostrar_dashboard():
    """
    Exibe o dashboard HTML legado, se necessário.
    """
    return send_file(REPORT_DIR / "index.html")

@app.route("/assets/<path:filename>")
def assets(filename: str):
    """
    Serve os arquivos estáticos do dashboard (imagens, CSS).
    """
    return send_from_directory(ASSETS_DIR, filename)

if __name__ == "__main__":
    app.run(debug=True)
