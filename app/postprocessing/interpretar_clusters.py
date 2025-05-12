import pandas as pd
import json
import traceback
from openai import OpenAI
import httpx
from dotenv import load_dotenv
import os
from collections import Counter

from app.config.paths import DATA_DIR, OUTPUTS_DIR

# Carrega variáveis de ambiente
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Cliente OpenAI com verificação de SSL desabilitada (para dev local)
client = OpenAI(api_key=api_key, http_client=httpx.Client(verify=False))


def gerar_resumo_cluster(df: pd.DataFrame, cluster_col: str, output_filename: str) -> None:
    clusters = df[cluster_col].dropna().unique()
    print(f"\n📊 Total de clusters a processar: {len(clusters)}")
    print(f"🧠 Iniciando análise de clusters para: {cluster_col}...\n")

    resumo_clusters = []

    for cluster_id in sorted(clusters):
        if int(cluster_id) == -1:
            print(f"🔸 Ignorando outlier (cluster -1)")
            continue

        print(f"➡️ Cluster {cluster_id}: processando...")
        subset = df[df[cluster_col] == cluster_id]

        # Determina tipo do cluster com base no status predominante
        status_counts = subset["status"].value_counts()
        tipo_cluster = "outros"
        if status_counts.get("closedwon", 0) >= status_counts.get("closedlost", 0) and status_counts.get("closedwon", 0) > 0:
            tipo_cluster = "sucesso"
        elif status_counts.get("closedlost", 0) > 0:
            tipo_cluster = "perda"

        # Coleta exemplos representativos (até 10)
        exemplos = []
        exemplos += subset[(subset["status"] == "closedwon") & (subset["motivo_sucesso"].notna())]["motivo_sucesso"].tolist()
        exemplos += subset[(subset["status"] == "closedlost") & (subset["motivo_perda"].notna())]["motivo_perda"].tolist()
        exemplos = [e for e in exemplos if isinstance(e, str) and e.strip()][:10]

        # Detecta motivo predominante
        motivos = exemplos.copy()
        palavras = " ".join(motivos).lower().split()
        palavras_uteis = [p for p in palavras if len(p) > 4]
        mais_frequente = Counter(palavras_uteis).most_common(1)
        palavra_chave = mais_frequente[0][0] if mais_frequente else ""

        # Gera bloco textual para prompt
        interacoes_texto = "\n".join(
            f"- Empresa: {row.get('empresa', '')} | "
            f"Status: {row.get('status', '')} | "
            f"Motivo: {(row.get('motivo_sucesso') if row.get('status') == 'closedwon' else row.get('motivo_perda')) or ''} | "
            f"Canal: {row.get('canal', '')}"
            for _, row in subset.head(8).iterrows()
        )

        prompt = f"""
Você é um especialista em inteligência comercial da Logcomex.
Receba abaixo interações agrupadas por semântica com leads reais.

Com base nas interações abaixo, responda em JSON com:
- "tema_detectado": Crie um título objetivo e específico com base no comportamento do cluster. Evite termos genéricos.
- "motivo_real": Por que esses leads avançam ou não
- "insight_estrategico": O que o time de vendas/marketing/produto pode aprender
- "exemplos_representativos": 2 frases desse cluster que representam bem o padrão

Interações:
{interacoes_texto}
"""

        try:
            resposta = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Você é um analista de vendas estratégico."},
                    {"role": "user", "content": prompt.strip()},
                ],
                temperature=0.2,
                max_tokens=600,
            )
            texto = resposta.choices[0].message.content.strip()

            try:
                dados = json.loads(texto)
                print(f"✅ Cluster {cluster_id}: análise gerada com sucesso.")
            except json.JSONDecodeError:
                print(f"⚠️ Cluster {cluster_id}: resposta inválida (não é JSON).")
                dados = {
                    "tema_detectado": f"Padrão com destaque para '{palavra_chave}'",
                    "motivo_real": texto,
                    "insight_estrategico": "",
                    "exemplos_representativos": exemplos[:2],
                }

        except Exception:
            print(f"\n❌ Cluster {cluster_id}: erro na requisição ao OpenAI")
            traceback.print_exc()
            dados = {
                "tema_detectado": f"Padrão com destaque para '{palavra_chave}'",
                "motivo_real": "",
                "insight_estrategico": "",
                "exemplos_representativos": exemplos[:2],
            }

        dados["cluster"] = int(cluster_id)
        dados["tipo_cluster"] = tipo_cluster
        resumo_clusters.append(dados)

    output_path = OUTPUTS_DIR / output_filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(resumo_clusters).to_csv(output_path, index=False)

    print(f"\n🎯 Análise final salva em: {output_path.resolve()}\n")


def carregar_insights_clusters() -> dict:
    insights = {}
    for algoritmo in ["kmeans", "hdbscan"]:
        file = OUTPUTS_DIR / f"analise_{algoritmo}.csv"
        if file.exists():
            df = pd.read_csv(file)
            insights[algoritmo] = df.to_dict(orient="records")
        else:
            insights[algoritmo] = []
    return insights


if __name__ == "__main__":
    df = pd.read_csv(DATA_DIR / "interacoes_clusterizadas.csv")
    gerar_resumo_cluster(df, cluster_col="cluster_kmeans", output_filename="analise_kmeans.csv")
    gerar_resumo_cluster(df, cluster_col="cluster_hdbscan", output_filename="analise_hdbscan.csv")
