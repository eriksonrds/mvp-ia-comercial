import os
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

# Carrega o token do arquivo .env
load_dotenv()
HUBSPOT_TOKEN = os.getenv("HUBSPOT_TOKEN")

# Endpoint da API de negócios (deals)
URL = "https://api.hubapi.com/crm/v3/objects/deals"

# Cabeçalhos com autenticação
HEADERS = {
    "Authorization": f"Bearer {HUBSPOT_TOKEN}",
    "Content-Type": "application/json"
}

# Campos desejados para análise estratégica
PROPERTIES = [
    "dealname",              # Nome do negócio
    "dealstage",             # Etapa do pipeline
    "pipeline",              # Qual pipeline de vendas está usando
    "description",           # Descrição ou observação do negócio
    "hubspot_owner_id",      # Responsável comercial interno
    "createdate",            # Quando o negócio foi criado
    "closedate",             # Quando foi fechado (se aplicável)
    "hs_lastmodifieddate",   # Última atualização
    "hs_source"              # Origem do negócio (se disponível)
    # ➕ você pode adicionar mais campos aqui conforme existirem no seu portal
]

def extrair_dados_hubspot(salvar_em="data/interacoes_hubspot.csv", limite=100):
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
            "ultima_interacao": prop.get("hs_lastmodifieddate", "")[:10] if prop.get("hs_lastmodifieddate") else ""
        })

    df = pd.DataFrame(dados)
    os.makedirs(os.path.dirname(salvar_em), exist_ok=True)
    df.to_csv(salvar_em, index=False)

    print(f"✅ Dados extraídos e salvos em: {salvar_em}")

if __name__ == "__main__":
    extrair_dados_hubspot()
