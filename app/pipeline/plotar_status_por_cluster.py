import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from app.config.paths import DATA_DIR, REPORT_DIR


def plotar_status_por_cluster(
    df_path: str = DATA_DIR / "interacoes_clusterizadas.csv",
    output_dir: str = REPORT_DIR / "assets",
) -> None:
    """
    Gera gráficos de barras com a distribuição dos status dos negócios por cluster.

    Args:
        df_path (str | Path): Caminho do CSV com os clusters e status.
        output_dir (str | Path): Diretório onde os gráficos serão salvos.
    """
    df = pd.read_csv(df_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    def gerar_plot(cluster_col: str, filename: str, titulo: str):
        plt.figure(figsize=(12, 8))
        agrupado = (
            df.groupby([cluster_col, "status"]).size().reset_index(name="quantidade")
        )

        sns.barplot(data=agrupado, x=cluster_col, y="quantidade", hue="status")

        plt.title(titulo)
        plt.xlabel("Cluster")
        plt.ylabel("Quantidade")
        plt.legend(
            title="Status do negócio",
            loc="upper center",
            bbox_to_anchor=(0.5, -0.12),
            ncol=3,
            frameon=False,
        )
        plt.tight_layout()
        plt.savefig(output_dir / filename, dpi=300)
        plt.close()

    print("📊 Gerando gráfico de status por cluster...")
    gerar_plot(
        "cluster_kmeans",
        "status_por_cluster_kmeans.png",
        "Distribuição de status por cluster (KMeans)",
    )
    gerar_plot(
        "cluster_hdbscan",
        "status_por_cluster_hdbscan.png",
        "Distribuição de status por cluster (HDBSCAN)",
    )

    print("✅ Gráficos salvos em:")
    print(f"   → {output_dir / 'status_por_cluster_kmeans.png'}")
    print(f"   → {output_dir / 'status_por_cluster_hdbscan.png'}")


if __name__ == "__main__":
    plotar_status_por_cluster()
