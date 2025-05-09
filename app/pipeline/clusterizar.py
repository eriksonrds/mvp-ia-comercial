import pandas as pd
from sklearn.cluster import KMeans
import hdbscan
from app.config.paths import DATA_DIR

def aplicar_clustering(
    input_path=DATA_DIR / "interacoes_com_embeddings.csv",
    output_path=DATA_DIR / "interacoes_clusterizadas.csv",
):
    """
    Aplica os algoritmos KMeans e HDBSCAN sobre os embeddings e salva os resultados.

    Args:
        input_path (Path): Caminho do CSV de entrada com embeddings.
        output_path (Path): Caminho onde será salvo o CSV com os clusters.
    """
    df = pd.read_csv(input_path)

    # Seleciona colunas de embedding
    embedding_cols = [col for col in df.columns if col.startswith("emb_")]
    X = df[embedding_cols].values

    # 🔹 KMeans
    print("🔹 Aplicando KMeans...")
    kmeans = KMeans(n_clusters=5, random_state=42, n_init="auto")
    df["cluster_kmeans"] = kmeans.fit_predict(X)
    print(f"✅ KMeans gerou {df['cluster_kmeans'].nunique()} clusters.")

    # 🔹 HDBSCAN
    print("🔹 Aplicando HDBSCAN...")
    hdb = hdbscan.HDBSCAN(min_cluster_size=3, min_samples=1, metric="euclidean")
    df["cluster_hdbscan"] = hdb.fit_predict(X)

    n_outliers = (df["cluster_hdbscan"] == -1).sum()
    n_clusters = df["cluster_hdbscan"].nunique() - (1 if -1 in df["cluster_hdbscan"].unique() else 0)

    print(f"✅ HDBSCAN gerou {n_clusters} clusters válidos e {n_outliers} outliers.")

    # Salva resultado
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"📁 Clusters salvos em: {output_path}")


if __name__ == "__main__":
    aplicar_clustering()
