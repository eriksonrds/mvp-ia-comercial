import pandas as pd
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

from app.config.paths import DATA_DIR, OUTPUTS_DIR, REPORT_DIR


def visualizar_tsne(
    input_path=DATA_DIR / "interacoes_clusterizadas.csv",
    output_dir=REPORT_DIR / "assets",
) -> None:
    """
    Reduz a dimensionalidade dos embeddings usando TSNE e gera visualizações 2D com anotações dos clusters.

    Args:
        input_path (Path): Caminho para o CSV com os dados e embeddings.
        output_dir (Path): Diretório onde os gráficos serão salvos.
    """
    df = pd.read_csv(input_path)
    embedding_cols = [col for col in df.columns if col.startswith("emb_")]
    X = df[embedding_cols].values

    print("🔄 Reduzindo dimensionalidade com TSNE...")
    tsne = TSNE(n_components=2, random_state=42, perplexity=10)
    X_2d = tsne.fit_transform(X)

    df["tsne_1"] = X_2d[:, 0]
    df["tsne_2"] = X_2d[:, 1]

    output_dir.mkdir(parents=True, exist_ok=True)

    def plot_clusters(cluster_col: str, filename: str, title: str, analise_path: Path):
        plt.figure(figsize=(12, 8))
        n_outliers = (df[cluster_col] == -1).sum()

        sns.scatterplot(
            x="tsne_1",
            y="tsne_2",
            hue=cluster_col,
            palette="tab10",
            data=df,
            s=80,
            alpha=0.85,
            edgecolor="black",
        )

        if -1 in df[cluster_col].values:
            title += f" (Outliers: {n_outliers})"

        try:
            analise_df = pd.read_csv(analise_path)
            for cluster_id in df[cluster_col].unique():
                if cluster_id == -1:
                    continue
                cluster_data = df[df[cluster_col] == cluster_id]
                cx = cluster_data["tsne_1"].mean()
                cy = cluster_data["tsne_2"].mean()

                tema = analise_df.loc[
                    analise_df["cluster"] == cluster_id, "tema_detectado"
                ].values
                if len(tema) > 0:
                    plt.text(
                        cx,
                        cy,
                        tema[0],
                        fontsize=9,
                        weight="bold",
                        ha="center",
                        va="center",
                        bbox=dict(
                            boxstyle="round,pad=0.3",
                            fc="white",
                            ec="black",
                            lw=1,
                            alpha=0.7,
                        ),
                    )
        except Exception as e:
            print(f"⚠️ Não foi possível anotar os temas: {e}")

        plt.title(title, fontsize=16)
        plt.xlabel("Dimensão 1 (TSNE)")
        plt.ylabel("Dimensão 2 (TSNE)")
        plt.legend(title="Cluster", bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.savefig(output_dir / filename, dpi=300)
        plt.close()

    print("📊 Gerando gráficos analíticos...")
    plot_clusters(
        "cluster_kmeans",
        "tsne_kmeans_com_tema.png",
        "Distribuição TSNE por KMeans",
        OUTPUTS_DIR / "analise_kmeans.csv",
    )
    plot_clusters(
        "cluster_hdbscan",
        "tsne_hdbscan_com_tema.png",
        "Distribuição TSNE por HDBSCAN",
        OUTPUTS_DIR / "analise_hdbscan.csv",
    )

    print("✅ Gráficos com temas salvos em:")
    print(f"   → {output_dir / 'tsne_kmeans_com_tema.png'}")
    print(f"   → {output_dir / 'tsne_hdbscan_com_tema.png'}")


if __name__ == "__main__":
    visualizar_tsne()
