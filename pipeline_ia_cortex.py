from app.services.gerar_dados_hubspot import extrair_dados_hubspot
from app.services.gerar_embeddings import gerar_embeddings_csv
from app.pipeline.clusterizar import aplicar_clustering
from app.postprocessing.preparar_dados_dashboard import preparar_dados_para_dashboard

def executar_pipeline_ia() -> None:
    """
    Executa o pipeline de preparação de dados brutos para o AI Córtex.
    """
    print("📌 Iniciando pipeline de preparação de dados para o AI Córtex...\n")

    try:
        extrair_dados_hubspot()
        gerar_embeddings_csv()
        aplicar_clustering()
        preparar_dados_para_dashboard()  # <<< adiciona isso
    except Exception as e:
        print(f"❌ Erro durante a execução da pipeline: {e}")
        return

    print("\n✅ Pipeline finalizado com sucesso.")
    print("📁 Arquivo principal gerado: data/interacoes_clusterizadas.csv")

if __name__ == "__main__":
    executar_pipeline_ia()
