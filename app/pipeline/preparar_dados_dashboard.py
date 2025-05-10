import pandas as pd
from app.utils.visualizar import visualizar_tsne
from app.pipeline.interpretar_clusters import gerar_resumo_cluster
from app.config.paths import DATA_DIR

def preparar_dados_para_dashboard():
    """
    Pipeline responsável por preparar os dados que alimentarão os dashboards do AI Córtex.

    Etapas:
        1. Visualização TSNE (adiciona colunas 'x' e 'y' ao CSV)
        2. Interpretação dos clusters via LLM (GPT)
        ---
        Os dados gerados serão utilizados pela rota '/dados' para alimentar os gráficos e insights no frontend.
    """
    print("📊 Iniciando preparação dos dados para o dashboard...\n")

    # Etapa 1 – Visualização com TSNE
    print("🔍 Gerando coordenadas TSNE...")
    visualizar_tsne()

    # Etapa 2 – Geração dos resumos com GPT
    print("🧠 Interpretando clusters com LLM...")
    df = pd.read_csv(DATA_DIR / "interacoes_clusterizadas.csv")

    gerar_resumo_cluster(df, "cluster_kmeans", "analise_kmeans.csv")
    gerar_resumo_cluster(df, "cluster_hdbscan", "analise_hdbscan.csv")

    print("\n✅ Dados para o dashboard prontos.")
    print("📁 Arquivos gerados: analise_kmeans.csv, analise_hdbscan.csv")


if __name__ == "__main__":
    preparar_dados_para_dashboard()

