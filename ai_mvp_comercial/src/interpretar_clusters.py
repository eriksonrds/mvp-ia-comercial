import pandas as pd
import os
import json
import traceback
from openai import OpenAI
from dotenv import load_dotenv
import httpx

# Carrega a chave da OpenAI
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Ignora verificação de certificado SSL (⚠️ apenas para ambiente local/teste)
client = OpenAI(
    api_key=api_key,
    http_client=httpx.Client(verify=False)
)

def gerar_resumo_cluster(df, cluster_col, output_path):
    clusters = df[cluster_col].unique()
    resumo_clusters = []

    for cluster_id in sorted(clusters):
        if cluster_id == -1:
            continue  # Ignora outliers do HDBSCAN

        subset = df[df[cluster_col] == cluster_id].copy()
        exemplos = subset.head(10)

        # Concatena exemplos completos com contexto
        interacoes_texto = "\n".join(
            f"- Empresa: {row.get('empresa', '')} | Descrição: {row.get('frase_interacao', '')} | Status: {row.get('status', '')} | Canal: {row.get('canal', '')}"
            for _, row in exemplos.iterrows()
        )

        prompt = f"""
            Você é um especialista em inteligência de mercado da Logcomex. Receberá registros reais de negócios agrupados por similaridade semântica.

            Com base nas interações abaixo, gere uma análise estruturada contendo:
            - "tema_detectado": qual é o assunto predominante nesse grupo.
            - "motivo_real": o que levou esses clientes a comprar ou considerar a compra.
            - "insight_estrategico": uma recomendação prática para vendas, marketing ou produto.
            - "exemplos_representativos": selecione 2 frases do grupo que representem bem o motivo.

            Responda apenas em formato JSON com as seguintes chaves:
            ["tema_detectado", "motivo_real", "insight_estrategico", "exemplos_representativos"]

            Interações:
            {interacoes_texto}
            """

        try:
            resposta = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Você é um analista de vendas estratégico."},
                    {"role": "user", "content": prompt.strip()}
                ],
                temperature=0.2,
                max_tokens=500
            )
            resposta_texto = resposta.choices[0].message.content.strip()

            try:
                resposta_json = json.loads(resposta_texto)
            except json.JSONDecodeError:
                print(f"⚠️ Resposta inválida em JSON no cluster {cluster_id}, salvando como texto bruto.")
                resposta_json = {
                    "tema_detectado": "Erro de parsing",
                    "motivo_real": resposta_texto,
                    "insight_estrategico": "",
                    "exemplos_representativos": []
                }

        except Exception as e:
            print(f"\n❌ Erro ao gerar resumo para o cluster {cluster_id}")
            print(f"→ Tipo de erro: {type(e).__name__}")
            print(f"→ Mensagem: {str(e)}")
            print("→ Traceback:")
            traceback.print_exc()

            resposta_json = {
                "tema_detectado": "Erro ao gerar resumo",
                "motivo_real": "",
                "insight_estrategico": "",
                "exemplos_representativos": []
            }

        resposta_json["cluster"] = cluster_id
        resumo_clusters.append(resposta_json)

    pd.DataFrame(resumo_clusters).to_csv(output_path, index=False)
    print(f"\n✅ Análise estratégica dos clusters salva em: {output_path}")

if __name__ == "__main__":
    df = pd.read_csv("data/interacoes_clusterizadas.csv")
    gerar_resumo_cluster(df, "cluster_kmeans", "outputs/analise_kmeans.csv")
    gerar_resumo_cluster(df, "cluster_hdbscan", "outputs/analise_hdbscan.csv")
