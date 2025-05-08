import pandas as pd
import random
from datetime import datetime
import os

# Função para gerar dados simulados de interações comerciais
def gerar_dados_simulados(qtd=50, salvar_em="data/interacoes_simuladas.csv"):
    # Gera nomes únicos de empresas fictícias
    nomes_empresas = [f"Empresa{str(i+1).zfill(2)}" for i in range(qtd)]
    canais = ["email", "call", "chat"]

    frases_ganhas = [
        "Fechamos por causa do suporte ágil.",
        "O onboarding foi muito rápido.",
        "Nos ajudaram com toda a parte burocrática.",
        "A plataforma é fácil de usar.",
        "Gostamos da integração com nosso ERP."
    ]

    frases_perdidas = [
        "O preço ficou acima do esperado.",
        "O atendimento demorou demais.",
        "Tivemos dificuldade em entender o produto.",
        "A equipe não respondeu no prazo.",
        "Faltaram funcionalidades essenciais."
    ]

    dados = []

    for i in range(qtd):
        status = random.choice(["ganho", "perdido"])
        frase = random.choice(frases_ganhas if status == "ganho" else frases_perdidas)
        linha = {
            "deal_id": i + 1,
            "empresa": nomes_empresas[i],  # empresa única por linha
            "status": status,
            "frase_interacao": frase,
            "canal": random.choice(canais),
            "data": datetime.now().strftime("%Y-%m-%d")
        }
        dados.append(linha)

    df = pd.DataFrame(dados)
    os.makedirs(os.path.dirname(salvar_em), exist_ok=True)
    df.to_csv(salvar_em, index=False)
    print(f"✅ Dados simulados salvos em: {salvar_em}")

if __name__ == "__main__":
    gerar_dados_simulados()
