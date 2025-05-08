import pandas as pd
import os
import traceback
from dotenv import load_dotenv
from openai import OpenAI
from time import sleep
import httpx

# Carrega a chave da OpenAI
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Cria cliente ignorando verificação de certificado SSL (⚠️ somente para ambiente local/teste)
client = OpenAI(
    api_key=api_key,
    http_client=httpx.Client(verify=False)
)

def gerar_embeddings_csv(input_path="data/interacoes_hubspot.csv", output_path="data/interacoes_com_embeddings.csv"):
    df = pd.read_csv(input_path)
    embeddings = []

    print("🔄 Gerando embeddings contextuais via OpenAI...\n")

    for i, row in df.iterrows():
        contexto = f"""
        Empresa: {row.get('empresa', '')}
        Descrição: {row.get('frase_interacao', '')}
        Status do negócio: {row.get('status', '')}
        Pipeline: {row.get('pipeline', '')}
        Data de criação: {row.get('data_criacao', '')}
        Data de fechamento: {row.get('data_fechamento', '')}
        Última interação: {row.get('ultima_interacao', '')}
        Responsável interno: {row.get('responsavel', '')}
        Canal de origem: {row.get('canal', '')}
        """

        sucesso = False
        for tentativa in range(3):
            try:
                response = client.embeddings.create(
                    model="text-embedding-3-small",
                    input=contexto.strip()
                )
                embedding = response.data[0].embedding
                sucesso = True
                break
            except Exception as e:
                print(f"\n⚠️ Tentativa {tentativa + 1} falhou para linha {i}")
                print(f"→ Tipo de erro: {type(e).__name__}")
                print(f"→ Mensagem: {str(e)}")
                print("→ Traceback:")
                traceback.print_exc()
                sleep(2 ** tentativa)

        if not sucesso:
            embedding = [0.0] * 1536
            print(f"❌ Falha definitiva ao gerar embedding para linha {i} — usando vetor nulo.")

        embeddings.append(embedding)

    # Criação do DataFrame de embeddings
    emb_df = pd.DataFrame(embeddings)
    emb_df.columns = [f"emb_{i}" for i in range(emb_df.shape[1])]
    df_emb = pd.concat([df, emb_df], axis=1)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_emb.to_csv(output_path, index=False)

    print(f"\n✅ Embeddings com contexto salvos em: {output_path}")

if __name__ == "__main__":
    gerar_embeddings_csv()
