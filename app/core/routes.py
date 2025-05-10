import pandas as pd
from flask import jsonify
from app.config.paths import DATA_DIR

@core_bp.route("/dados")
def dados():
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
