from flask import Blueprint, render_template, jsonify, request
import pandas as pd
import subprocess
from app.config.paths import DATA_DIR
from app.presentation.plotar_status_por_cluster import gerar_status_por_cluster_dados
from app.postprocessing.interpretar_clusters import carregar_insights_clusters

core_bp = Blueprint(
    "core",
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

@core_bp.route("/")
def index():
    return render_template("index.html", gerando=False)

@core_bp.route("/insights")
def reports():
    return render_template("insights.html")

@core_bp.route("/dados")
def dados():
    df = pd.read_csv(DATA_DIR / "interacoes_clusterizadas.csv")

    TRADUCAO_MOTIVOS = {
        "closedwon": "Negócio Fechado",
        "closedlost": "Negócio Perdido",
        "contractsent": "Contrato Enviado",
        "presentationscheduled": "Apresentação Agendada",
        "qualifiedtobuy": "Lead Qualificado",
        "decisionmakerboughtin": "Decisor Engajado"
    }

    # Leads por status (gráfico de barras)
    barras = df["status"].value_counts().reset_index()
    barras.columns = ["status", "quantidade"]
    barras["status"] = barras["status"].map(TRADUCAO_MOTIVOS).fillna(barras["status"])
    barras = barras.to_dict(orient="records")

    # Coordenadas 2D dos clusters para gráfico de dispersão (kmeans)
    clusters = df.groupby("cluster_kmeans")[["tsne_1", "tsne_2"]].apply(
        lambda g: g.values.tolist()).to_dict()

    # Leitura dos temas detectados por cluster
    try:
        analise = pd.read_csv(DATA_DIR.parent / "outputs" / "analise_kmeans.csv")
        nomes_clusters = analise.set_index("cluster")["tema_detectado"].to_dict()
    except Exception:
        nomes_clusters = {}

    # Distribuição de status por cluster (tabela complementar)
    status_por_cluster = gerar_status_por_cluster_dados()

    # Insights extraídos pelo modelo
    insights = carregar_insights_clusters()

    # Tratamento de exemplos para visualização
    for item in insights.get("kmeans", []):
        exemplos_raw = item.get("exemplos_representativos", [])
        if isinstance(exemplos_raw, str):
            try:
                exemplos = eval(exemplos_raw)
            except:
                exemplos = exemplos_raw.replace("[", "").replace("]", "").split("', '")
                exemplos = [e.replace("'", "").strip() for e in exemplos]
        else:
            exemplos = exemplos_raw

        exemplos_formatados = []
        for exemplo in exemplos:
            if isinstance(exemplo, dict):
                empresa = exemplo.get("empresa", "-")
                descricao = exemplo.get("descricao", "-")
                status = exemplo.get("status", "-")
                canal = exemplo.get("canal", "-")
                linha = f"• Empresa: {empresa} | Descrição: {descricao} | Status: {status} | Canal: {canal}"
                exemplos_formatados.append(linha)
            else:
                exemplos_formatados.append(f"• {exemplo}")

        item["exemplos_representativos"] = exemplos_formatados
        item["tema_detectado"] = nomes_clusters.get(item["cluster"], f"Cluster {item['cluster']}")

    # Motivos reais de sucesso e perda
    motivos_sucesso = df["motivo_sucesso"].dropna().value_counts().reset_index()
    motivos_sucesso.columns = ["motivo", "quantidade"]
    motivos_sucesso = motivos_sucesso.to_dict(orient="records")

    motivos_perda = df["motivo_perda"].dropna().value_counts().reset_index()
    motivos_perda.columns = ["motivo", "quantidade"]
    motivos_perda = motivos_perda.to_dict(orient="records")

    # Conversão de datas
    df["data_criacao"] = pd.to_datetime(df["data_criacao"], errors="coerce")
    df["data_fechamento"] = pd.to_datetime(df["data_fechamento"], errors="coerce")

    # Negócios criados por mês
    negocios_por_mes = df["data_criacao"].dt.to_period("M").value_counts().sort_index()
    negocios_por_mes = negocios_por_mes.reset_index()
    negocios_por_mes.columns = ["mes", "quantidade"]
    negocios_por_mes["mes"] = negocios_por_mes["mes"].astype(str)
    negocios_por_mes = negocios_por_mes.to_dict(orient="records")

    # Negócios fechados por mês
    negocios_fechados_por_mes = df["data_fechamento"].dt.to_period("M").value_counts().sort_index()
    negocios_fechados_por_mes = negocios_fechados_por_mes.reset_index()
    negocios_fechados_por_mes.columns = ["mes", "quantidade"]
    negocios_fechados_por_mes["mes"] = negocios_fechados_por_mes["mes"].astype(str)
    negocios_fechados_por_mes = negocios_fechados_por_mes.to_dict(orient="records")

    return jsonify({
        "barras": barras,
        "clusters": clusters,
        "nomes_clusters": nomes_clusters,
        "status_por_cluster": status_por_cluster,
        "insights": insights,
        "motivos_sucesso": motivos_sucesso,
        "motivos_perda": motivos_perda,
        "negocios_por_mes": negocios_por_mes,
        "negocios_fechados_por_mes": negocios_fechados_por_mes
    })

@core_bp.route("/executar-pipeline", methods=["POST"])
def executar_pipeline():
    try:
        subprocess.run(["python", "pipeline_ia_cortex.py"], check=True)
        return jsonify({"status": "ok", "mensagem": "Pipeline executada com sucesso"})
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500
