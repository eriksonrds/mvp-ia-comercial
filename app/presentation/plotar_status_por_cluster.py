import pandas as pd
from app.config.paths import DATA_DIR

TRADUCAO_MOTIVOS = {
    "closedwon": "Negócio Fechado",
    "closedlost": "Negócio Perdido",
    "contractsent": "Contrato Enviado",
    "presentationscheduled": "Apresentação Agendada",
    "qualifiedtobuy": "Lead Qualificado",
    "decisionmakerboughtin": "Decisor Engajado"
}

def gerar_status_por_cluster_dados(
    df_path: str = DATA_DIR / "interacoes_clusterizadas.csv",
    cluster_cols: list[str] = ["cluster_kmeans", "cluster_hdbscan"]
) -> dict:
    """
    Gera a distribuição de status por cluster, agrupando por algoritmo.

    Returns:
        dict: {
            "cluster_kmeans": [{cluster, status, quantidade}, ...],
            "cluster_hdbscan": [...]
        }
    """
    df = pd.read_csv(df_path)
    resultado = {}

    for cluster_col in cluster_cols:
        agrupado = (
            df.groupby([cluster_col, "status"])
            .size()
            .reset_index(name="quantidade")
        )

        agrupado[cluster_col] = agrupado[cluster_col].astype(int)
        agrupado["status"] = agrupado["status"].map(TRADUCAO_MOTIVOS).fillna(agrupado["status"])
        resultado[cluster_col] = agrupado.to_dict(orient="records")

    return resultado


# Execução direta (debug)
if __name__ == "__main__":
    from pprint import pprint
    pprint(gerar_status_por_cluster_dados())
