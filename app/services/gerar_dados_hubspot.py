import pandas as pd
import requests
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

PROPERTIES = [
    "dealname",                    # Nome do negócio
    "dealstage",                  # Etapa do negócio
    "pipeline",                   # Pipeline    
    "hubspot_owner_id",           # Proprietário (ID)
    "createdate",                 # Data de criação
    "closedate",                  # Data de fechamento
    "hs_lastmodifieddate",        # Última modificação
    "hs_source",                  # Canal de origem (se disponível)
    "closed_won_reason",          # Motivo de sucesso (padrão HubSpot)
    "closed_lost_reason"          # Motivo de perda (padrão HubSpot)
]



def extrair_dados_hubspot(salvar_em=DATA_DIR / "interacoes_hubspot.csv", limite=100):
    """
    Extrai dados da API do HubSpot e salva em CSV para posterior análise.
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
            "motivo_sucesso": prop.get("closed_won_reason", ""),
            "motivo_perda": prop.get("closed_lost_reason", ""),
            "responsavel": prop.get("hubspot_owner_id", ""),
            "data_criacao": prop.get("createdate", "")[:10],
            "data_fechamento": prop.get("closedate", "")[:10] if prop.get("closedate") else "",
            "ultima_interacao": prop.get("hs_lastmodifieddate", "")[:10] if prop.get("hs_lastmodifieddate") else ""
        })

    df = pd.DataFrame(dados)
    salvar_em.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(salvar_em, index=False)

    print(f"✅ Dados extraídos e salvos em: {salvar_em}")


if __name__ == "__main__":
    extrair_dados_hubspot()
