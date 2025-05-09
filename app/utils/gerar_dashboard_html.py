from datetime import datetime
from pathlib import Path
import pandas as pd

from app.config.paths import REPORT_DIR, OUTPUTS_DIR, REPORT_DIR


def gerar_dashboard_html() -> None:
    """
    Gera um dashboard HTML visualizando os resultados de análise por cluster.

    Inclui imagens, tabelas e metadados das análises feitas por KMeans e HDBSCAN.
    """
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    assets_path = "assets"
    html_path = REPORT_DIR / "index.html"

    analise_kmeans = pd.read_csv(OUTPUTS_DIR / "analise_kmeans.csv").to_html(index=False, classes="tabela")
    analise_hdbscan = pd.read_csv(OUTPUTS_DIR / "analise_hdbscan.csv").to_html(index=False, classes="tabela")

    def imagem_dupla(img1, img2, legenda1, legenda2):
        return f'''
        <div class="row">
            <div class="card">
                <h4>{legenda1}</h4>
                <img src="{assets_path}/{img1}" alt="{legenda1}">
            </div>
            <div class="card">
                <h4>{legenda2}</h4>
                <img src="{assets_path}/{img2}" alt="{legenda2}">
            </div>
        </div>
        '''

    html = f'''
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>Dashboard de Inteligência Comercial</title>
        <link rel="stylesheet" href="{assets_path}/style.css">
    </head>
    <body>
        <div class="container">
            <header class="header">
                <h1>Dashboard de Inteligência Comercial</h1>
                <p><strong>Data de geração:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
                <p>Este relatório apresenta a análise automatizada de clusters de interações comerciais, identificando temas centrais, motivos reais de compra e insights estratégicos.</p>
            </header>

            <section>
                <h2>🔹 Visualização TSNE + Status (KMeans)</h2>
                {imagem_dupla("tsne_kmeans_com_tema.png", "status_por_cluster_kmeans.png", "TSNE com temas por KMeans", "Status por cluster (KMeans)")}
                {analise_kmeans}
            </section>

            <section>
                <h2>🔹 Visualização TSNE + Status (HDBSCAN)</h2>
                {imagem_dupla("tsne_hdbscan_com_tema.png", "status_por_cluster_hdbscan.png", "TSNE com temas por HDBSCAN", "Status por cluster (HDBSCAN)")}
                {analise_hdbscan}
            </section>
        </div>

        <script>
            function ajustarAltura() {{
                const altura = document.body.scrollHeight;
                window.parent.postMessage({{ tipo: "ajustarAltura", altura: altura }}, "*");
            }}
            window.onload = ajustarAltura;
            window.onresize = ajustarAltura;
        </script>
    </body>
    </html>
    '''

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Dashboard HTML salvo em: {html_path}")


if __name__ == "__main__":
    gerar_dashboard_html()
