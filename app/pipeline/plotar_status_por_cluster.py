import pandas as pd
from app.config.paths import DATA_DIR

def gerar_status_por_cluster_dados(
    df_path: str = DATA_DIR / "interacoes_clusterizadas.csv",
    cluster_cols: list[str] = ["cluster_kmeans", "cluster_hdbscan"]
) -> dict:
    """
    Gera dados agregados com a distribuição de status por cluster.

    Args:
        df_path (Path): Caminho do arquivo CSV com os dados clusterizados.
        cluster_cols (list[str]): Lista de colunas de cluster a serem processadas.

    Returns:
        dict: Dados por coluna de cluster, no formato:
            {
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

        resultado[cluster_col] = agrupado.to_dict(orient="records")

    return resultado


# Exemplo de uso (debug/teste)
if __name__ == "__main__":
    dados = gerar_status_por_cluster_dados()
    from pprint import pprint
    pprint(dados)
