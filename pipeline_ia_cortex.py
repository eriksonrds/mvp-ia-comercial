from app.services.gerar_dados_hubspot import extrair_dados_hubspot
from app.services.gerar_embeddings import gerar_embeddings_csv
from app.pipeline.clusterizar import aplicar_clustering

def executar_pipeline_ia() -> None:
    """
    Executa o pipeline de preparação de dados brutos para o AI Córtex.

    Etapas:
        1. Extração de dados via HubSpot
        2. Geração de embeddings com OpenAI
        3. Clustering dos embeddings (KMeans e HDBSCAN)
    """
    print("📌 Iniciando pipeline de preparação de dados para o AI Córtex...\n")

    # Etapa 1 – Extração via HubSpot
    extrair_dados_hubspot()

    # Etapa 2 – Geração de embeddings via OpenAI
    gerar_embeddings_csv()

    # Etapa 3 – Clustering dos embeddings
    aplicar_clustering()

    print("\n✅ Pipeline finalizado com sucesso.")
    print("📁 Arquivo principal gerado: data/interacoes_clusterizadas.csv")


if __name__ == "__main__":
    executar_pipeline_ia()
