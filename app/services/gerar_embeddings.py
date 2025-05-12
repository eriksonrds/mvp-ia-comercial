import pandas as pd
import traceback
from time import sleep
import httpx
from openai import OpenAI
from dotenv import load_dotenv
import os

from app.config.paths import DATA_DIR

# Carrega variáveis de ambiente
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Cria cliente ignorando SSL (ambiente local/teste)
client = OpenAI(api_key=api_key, http_client=httpx.Client(verify=False))

def gerar_embeddings_csv(
    input_path=DATA_DIR / "interacoes_hubspot.csv",
    output_path=DATA_DIR / "interacoes_com_embeddings.csv",
) -> None:
    """
    Gera embeddings com base nos dados estruturados do HubSpot e salva em CSV.
    """
    df = pd.read_csv(input_path)
    embeddings = []

    print("🔄 Gerando embeddings contextuais via OpenAI...\n")

    for i, row in df.iterrows():
        contexto = f"""
        Empresa: {row.get('empresa', '')}
        Status do negócio: {row.get('status', '')}
        Pipeline: {row.get('pipeline', '')}
        Motivo de sucesso: {row.get('motivo_sucesso', '')}
        Motivo de perda: {row.get('motivo_perda', '')}
        Data de criação: {row.get('data_criacao', '')}
        Data de fechamento: {row.get('data_fechamento', '')}
        Última interação: {row.get('ultima_interacao', '')}
        Responsável: {row.get('responsavel', '')}
        """

        sucesso = False
        for tentativa in range(3):
            try:
                response = client.embeddings.create(
                    model="text-embedding-3-small", input=contexto.strip()
                )
                embedding = response.data[0].embedding
                sucesso = True
                break
            except Exception as e:
                print(f"\n⚠️ Tentativa {tentativa + 1} falhou para linha {i}")
                print(f"→ Tipo de erro: {type(e).__name__}")
                print(f"→ Mensagem: {str(e)}")
                traceback.print_exc()
                sleep(2**tentativa)

        if not sucesso:
            embedding = [0.0] * 1536
            print(f"❌ Falha definitiva ao gerar embedding para linha {i} — usando vetor nulo.")

        embeddings.append(embedding)

    emb_df = pd.DataFrame(embeddings)
    emb_df.columns = [f"emb_{i}" for i in range(emb_df.shape[1])]
    df_emb = pd.concat([df, emb_df], axis=1)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_emb.to_csv(output_path, index=False)

    print(f"\n✅ Embeddings com contexto salvos em: {output_path}")

if __name__ == "__main__":
    gerar_embeddings_csv()
