from flask import Blueprint, render_template, jsonify
import pandas as pd
from app.config.paths import DATA_DIR
from app.pipeline.plotar_status_por_cluster import gerar_status_por_cluster_dados
from app.pipeline.interpretar_clusters import carregar_insights_clusters

core_bp = Blueprint(
    "core",
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

@core_bp.route("/")
def index():
    """
    Rota principal - dashboard com gráficos (sem insights).
    """
    return render_template("index.html", gerando=False)


@core_bp.route("/reports")
def reports():
    """
    Rota da página de relatórios com insights estratégicos.
    """
    return render_template("reports.html")


@core_bp.route("/dados")
def dados():
    """
    API com os dados necessários para os dashboards e relatórios.
    """
    df = pd.read_csv(DATA_DIR / "interacoes_clusterizadas.csv")

    # Leads por status (barras)
    barras = df["status"].value_counts().reset_index()
    barras.columns = ["status", "quantidade"]
    barras = barras.to_dict(orient="records")

    # Clusters TSNE
    clusters = df.groupby("cluster_kmeans")[["tsne_1", "tsne_2"]].apply(
        lambda g: g.values.tolist()).to_dict()

    # Distribuição de status por cluster
    status_por_cluster = gerar_status_por_cluster_dados()

    # Insights estratégicos por cluster (via GPT)
    insights = carregar_insights_clusters()

    return jsonify({
        "barras": barras,
        "clusters": clusters,
        "status_por_cluster": status_por_cluster,
        "insights": insights
    })
