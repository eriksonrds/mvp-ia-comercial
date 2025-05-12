import pandas as pd
from sklearn.cluster import KMeans
import hdbscan
from app.config.paths import DATA_DIR


def aplicar_clustering(
    input_path=DATA_DIR / "interacoes_com_embeddings.csv",
    output_path=DATA_DIR / "interacoes_clusterizadas.csv",
):
    """
    Aplica os algoritmos KMeans e HDBSCAN sobre os embeddings das interações e salva os clusters.

    Args:
        input_path (Path): CSV de entrada com embeddings e metadados.
        output_path (Path): Caminho onde será salvo o CSV com os clusters atribuídos.
    """
    df = pd.read_csv(input_path)

    # Seleciona somente colunas de embedding (ex: emb_0, emb_1, ..., emb_1535)
    embedding_cols = [col for col in df.columns if col.startswith("emb_")]
    X = df[embedding_cols].values

    # 🔹 KMeans
    print("🔹 Aplicando KMeans...")
    kmeans = KMeans(n_clusters=6, random_state=42, n_init="auto")  # Ajustável
    df["cluster_kmeans"] = kmeans.fit_predict(X)
    print(f"✅ KMeans criou {df['cluster_kmeans'].nunique()} clusters.")

    # 🔹 HDBSCAN (opcional, para validação e análise de densidade)
    print("🔹 Aplicando HDBSCAN...")
    hdb = hdbscan.HDBSCAN(min_cluster_size=3, min_samples=1, metric="euclidean")
    df["cluster_hdbscan"] = hdb.fit_predict(X)

    n_outliers = (df["cluster_hdbscan"] == -1).sum()
    n_clusters = df["cluster_hdbscan"].nunique() - (
        1 if -1 in df["cluster_hdbscan"].unique() else 0
    )
    print(f"✅ HDBSCAN identificou {n_clusters} clusters válidos e {n_outliers} outliers.")

    # Salva resultado com os clusters
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"📁 Arquivo salvo com clusters: {output_path}")


if __name__ == "__main__":
    aplicar_clustering()
