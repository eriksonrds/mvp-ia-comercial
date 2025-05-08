import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def plotar_status_por_cluster(df_path="data/interacoes_clusterizadas.csv", output_dir="report/assets"):
    df = pd.read_csv(df_path)
    os.makedirs(output_dir, exist_ok=True)

    def gerar_plot(cluster_col, filename, titulo):
        plt.figure(figsize=(12, 8))
        agrupado = df.groupby([cluster_col, "status"]).size().reset_index(name="quantidade")

        sns.barplot(
            data=agrupado,
            x=cluster_col,
            y="quantidade",
            hue="status"
        )

        plt.title(titulo)
        plt.xlabel("Cluster")
        plt.ylabel("Quantidade")
        plt.legend(title="Status do negócio", loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=3, frameon=False)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, filename), dpi=300)
        plt.close()

    print("📊 Gerando gráfico de status por cluster...")
    gerar_plot("cluster_kmeans", "status_por_cluster_kmeans.png", "Distribuição de status por cluster (KMeans)")
    gerar_plot("cluster_hdbscan", "status_por_cluster_hdbscan.png", "Distribuição de status por cluster (HDBSCAN)")
    print("✅ Gráficos salvos em:")
    print(f"   → {output_dir}/status_por_cluster_kmeans.png")
    print(f"   → {output_dir}/status_por_cluster_hdbscan.png")

if __name__ == "__main__":
    plotar_status_por_cluster()
