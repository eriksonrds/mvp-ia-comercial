from src.gerar_dados_hubspot import extrair_dados_hubspot
from src.gerar_embeddings import gerar_embeddings_csv
from src.clusterizar import aplicar_clustering
from src.visualizar import visualizar_tsne
from src.interpretar_clusters import gerar_resumo_cluster
from src.plotar_status_por_cluster import plotar_status_por_cluster
from src.gerar_dashboard_html import gerar_dashboard_html  # ✅ Etapa final

import pandas as pd

def main():
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
    df = pd.read_csv("data/interacoes_clusterizadas.csv")
    gerar_resumo_cluster(df, "cluster_kmeans", "outputs/analise_kmeans.csv")
    gerar_resumo_cluster(df, "cluster_hdbscan", "outputs/analise_hdbscan.csv")

    # Etapa 6 – Gráficos de performance por cluster
    plotar_status_por_cluster()

    # Etapa 7 – Geração do dashboard HTML final
    gerar_dashboard_html()

    print("\n✅ Pipeline finalizado com sucesso.")
    print("📁 Relatório disponível em: report/index.html")

if __name__ == "__main__":
    main()
