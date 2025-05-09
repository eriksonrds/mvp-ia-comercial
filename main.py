from app.services.gerar_dados_hubspot import extrair_dados_hubspot
from app.services.gerar_embeddings import gerar_embeddings_csv
from app.pipeline.clusterizar import aplicar_clustering
from app.utils.visualizar import visualizar_tsne
from app.pipeline.interpretar_clusters import gerar_resumo_cluster
from app.pipeline.plotar_status_por_cluster import plotar_status_por_cluster
from app.utils.gerar_dashboard_html import gerar_dashboard_html

from app.config.paths import DATA_DIR
import pandas as pd


def main() -> None:
    """
    Executa o pipeline completo de inteligência comercial baseado em interações reais.

    Etapas:
        1. Extração de dados via HubSpot
        2. Geração de embeddings com OpenAI
        3. Clustering dos embeddings (KMeans e HDBSCAN)
        4. Visualização TSNE com anotação de temas
        5. Interpretação dos clusters via LLM
        6. Gráficos de status por cluster
        7. Geração de dashboard HTML
    """
    print("📌 Iniciando pipeline completo de IA comercial...\n")

    # Etapa 1 – Extração via HubSpot
    extrair_dados_hubspot()

    # Etapa 2 – Geração de embeddings via OpenAI
    gerar_embeddings_csv()

    # Etapa 3 – Clustering dos embeddings
    aplicar_clustering()

    # Etapa 4 – Visualização com TSNE
    visualizar_tsne()

    # Etapa 5 – Interpretação dos clusters
    df = pd.read_csv(DATA_DIR / "interacoes_clusterizadas.csv")
    gerar_resumo_cluster(df, "cluster_kmeans", "analise_kmeans.csv")
    gerar_resumo_cluster(df, "cluster_hdbscan", "analise_hdbscan.csv")

    # Etapa 6 – Gráficos de performance por cluster
    plotar_status_por_cluster()

    # Etapa 7 – Geração do dashboard HTML final
    gerar_dashboard_html()

    print("\n✅ Pipeline finalizado com sucesso.")
    print("📁 Relatório disponível em: report/index.html")


if __name__ == "__main__":
    main()
