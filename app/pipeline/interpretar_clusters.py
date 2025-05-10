import pandas as pd
import json
import traceback
from openai import OpenAI
import httpx
from dotenv import load_dotenv
import os

from app.config.paths import DATA_DIR, OUTPUTS_DIR

# Carrega variáveis de ambiente
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Instância segura do cliente OpenAI (sem verificação de certificado para dev)
client = OpenAI(api_key=api_key, http_client=httpx.Client(verify=False))


def gerar_resumo_cluster(
    df: pd.DataFrame, cluster_col: str, output_filename: str
) -> None:
    """
    Gera um resumo estratégico por cluster a partir de interações agrupadas.

    Args:
        df (pd.DataFrame): DataFrame com as interações e coluna de cluster.
        cluster_col (str): Nome da coluna de cluster a ser analisada.
        output_filename (str): Nome do arquivo CSV de saída (será salvo em OUTPUTS_DIR).
    """
    clusters = df[cluster_col].unique()
    resumo_clusters = []

    for cluster_id in sorted(clusters):
        if cluster_id == -1:
            continue  # Ignora outliers (HDBSCAN)

        subset = df[df[cluster_col] == cluster_id]
        exemplos = subset.head(10)

        interacoes_texto = "\n".join(
            f"- Empresa: {row.get('empresa', '')} | "
            f"Descrição: {row.get('frase_interacao', '')} | "
            f"Status: {row.get('status', '')} | "
            f"Canal: {row.get('canal', '')}"
            for _, row in exemplos.iterrows()
        )

        prompt = (
            "Você é um especialista em inteligência de mercado da Logcomex. "
            "Receberá registros reais de negócios agrupados por similaridade semântica.\n\n"
            "Com base nas interações abaixo, gere uma análise estruturada contendo:\n"
            '- "tema_detectado": qual é o assunto predominante nesse grupo.\n'
            '- "motivo_real": o que levou esses clientes a comprar ou considerar a compra.\n'
            '- "insight_estrategico": uma recomendação prática para vendas, marketing ou produto.\n'
            '- "exemplos_representativos": selecione 2 frases do grupo que representem bem o motivo.\n\n'
            "Responda apenas em formato JSON com as seguintes chaves:\n"
            '["tema_detectado", "motivo_real", "insight_estrategico", "exemplos_representativos"]\n\n'
            f"Interações:\n{interacoes_texto}"
        )

        try:
            resposta = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um analista de vendas estratégico.",
                    },
                    {"role": "user", "content": prompt.strip()},
                ],
                temperature=0.2,
                max_tokens=500,
            )
            resposta_texto = resposta.choices[0].message.content.strip()

            try:
                resposta_json = json.loads(resposta_texto)
            except json.JSONDecodeError:
                print(
                    f"⚠️ Resposta inválida no cluster {cluster_id}. "
                    "Salvando como texto bruto."
                )
                resposta_json = {
                    "tema_detectado": "Erro de parsing",
                    "motivo_real": resposta_texto,
                    "insight_estrategico": "",
                    "exemplos_representativos": [],
                }

        except Exception:
            print(f"\n❌ Erro ao gerar resumo para o cluster {cluster_id}")
            traceback.print_exc()
            resposta_json = {
                "tema_detectado": "Erro ao gerar resumo",
                "motivo_real": "",
                "insight_estrategico": "",
                "exemplos_representativos": [],
            }

        resposta_json["cluster"] = cluster_id
        resumo_clusters.append(resposta_json)

    # Exporta o resultado
    output_path = OUTPUTS_DIR / output_filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(resumo_clusters).to_csv(output_path, index=False)
    print(f"\n✅ Análise dos clusters salva em: {output_path}")


def carregar_insights_clusters() -> dict:
    """
    Lê os arquivos CSV de análise por cluster e retorna como dicionário para o frontend.

    Returns:
        dict: {
            "kmeans": [ {cluster, tema_detectado, ...}, ... ],
            "hdbscan": [ {...}, ... ]
        }
    """
    insights = {}
    for algoritmo in ["kmeans", "hdbscan"]:
        file = OUTPUTS_DIR / f"analise_{algoritmo}.csv"
        if file.exists():
            df = pd.read_csv(file)
            insights[algoritmo] = df.to_dict(orient="records")
        else:
            insights[algoritmo] = []
    return insights

