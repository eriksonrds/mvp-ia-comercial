from app.services.gerar_dados_hubspot import extrair_dados_hubspot
from app.services.gerar_embeddings import gerar_embeddings_csv
from app.pipeline.clusterizar import aplicar_clustering
from app.utils.visualizar import visualizar_tsne
from app.pipeline.interpretar_clusters import gerar_resumo_cluster
from app.config.paths import DATA_DIR
import pandas as pd

def executar_pipeline_ia() -> None:
    """
    Executa o pipeline de preparação de dados para o AI Córtex.

    Etapas:
        1. Extração de dados via HubSpot
        2. Geração de embeddings com OpenAI
        3. Clustering dos embeddings (KMeans e HDBSCAN)
        4. Visualização TSNE com anotação de temas
        5. Interpretação dos clusters via LLM
    """
    print("📌 Iniciando pipeline de preparação de dados para o AI Córtex...\n")

    # Etapa 1 – Extração via HubSpot
    extrair_dados_hubspot()

    # Etapa 2 – Geração de embeddings via OpenAI
    gerar_embeddings_csv()

    # Etapa 3 – Clustering dos embeddings
    aplicar_clustering()

    # Etapa 4 – Visualização com TSNE
    visualizar_tsne()

    # Etapa 5 – Interpretação dos clusters com GPT
    df = pd.read_csv(DATA_DIR / "interacoes_clusterizadas.csv")
    gerar_resumo_cluster(df, "cluster_kmeans", "analise_kmeans.csv")
    gerar_resumo_cluster(df, "cluster_hdbscan", "analise_hdbscan.csv")

    print("\n✅ Pipeline finalizado com sucesso.")
    print("📁 Arquivos prontos para visualização no AI Córtex.")


if __name__ == "__main__":
    executar_pipeline_ia()
