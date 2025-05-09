import pandas as pd
import requests
from datetime import datetime
from dotenv import load_dotenv
import os

from app.config.paths import DATA_DIR

# Carrega variáveis de ambiente
load_dotenv()
HUBSPOT_TOKEN = os.getenv("HUBSPOT_TOKEN")

# Endpoint e cabeçalhos
URL = "https://api.hubapi.com/crm/v3/objects/deals"
HEADERS = {
    "Authorization": f"Bearer {HUBSPOT_TOKEN}",
    "Content-Type": "application/json",
}

# Propriedades desejadas
PROPERTIES = [
    "dealname",
    "dealstage",
    "pipeline",
    "description",
    "hubspot_owner_id",
    "createdate",
    "closedate",
    "hs_lastmodifieddate",
    "hs_source",
]


def extrair_dados_hubspot(salvar_em=DATA_DIR / "interacoes_hubspot.csv", limite=100) -> None:
    """
    Extrai dados da API do HubSpot e salva em CSV para posterior análise.

    Args:
        salvar_em (Path): Caminho do arquivo de saída.
        limite (int): Número máximo de registros a extrair.
    """
    print("🔄 Extraindo dados da API do HubSpot...")

    params = {
        "limit": limite,
        "properties": ",".join(PROPERTIES),
    }

    response = requests.get(URL, headers=HEADERS, params=params)

    if response.status_code != 200:
        print(f"❌ Erro {response.status_code}: {response.text}")
        return

    resultados = response.json().get("results", [])
    dados = []

    for r in resultados:
        prop = r.get("properties", {})
        dados.append({
            "deal_id": r.get("id"),
            "empresa": prop.get("dealname", ""),
            "status": prop.get("dealstage", ""),
            "pipeline": prop.get("pipeline", ""),
            "frase_interacao": prop.get("description", ""),
            "responsavel": prop.get("hubspot_owner_id", ""),
            "canal": prop.get("hs_source", ""),
            "data_criacao": prop.get("createdate", "")[:10],
            "data_fechamento": prop.get("closedate", "")[:10] if prop.get("closedate") else "",
            "ultima_interacao": prop.get("hs_lastmodifieddate", "")[:10] if prop.get("hs_lastmodifieddate") else "",
        })

    df = pd.DataFrame(dados)
    salvar_em.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(salvar_em, index=False)

    print(f"✅ Dados extraídos e salvos em: {salvar_em}")


if __name__ == "__main__":
    extrair_dados_hubspot()
