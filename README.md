# MVP – IA Aplicada à Inteligência Comercial | Logcomex

Este projeto demonstra um MVP funcional de aplicação de **Inteligência Artificial** para identificar os **reais motivos por trás das vendas ganhas e perdidas**, com foco em análise de interações de clientes e geração de insights estratégicos para a área comercial da **Logcomex**.

---

## Objetivo

Desenvolver uma solução baseada em IA que seja capaz de extrair, interpretar e agrupar, por similaridade semântica, as razões que levam à conversão ou perda de clientes. A proposta visa apoiar decisões estratégicas, otimizar abordagens de vendas e aumentar a retenção de clientes.

---

## Visão Geral da Solução

O pipeline implementado neste projeto realiza:

1. **Extração de dados reais via API do HubSpot** (negócios + interações).
2. **Geração de embeddings semânticos** com a API da OpenAI.
3. **Clusterização** com KMeans e HDBSCAN para agrupar motivos de compra/perda.
4. **Visualização dos clusters** com TSNE em gráficos 2D.
5. **Interpretação automática dos clusters** com GPT-4.
6. **Geração de dashboards interativos e relatórios CSV.**

---

## Tecnologias Utilizadas

| Categoria           | Ferramentas / Tecnologias                |
| ------------------- | ---------------------------------------- |
| Linguagem principal | Python                                   |
| IA e NLP            | OpenAI Embeddings, GPT-4                 |
| Clustering          | Scikit-learn (KMeans), HDBSCAN           |
| Visualização        | Matplotlib, Seaborn, TSNE                |
| Web                 | Flask (Interface interativa)             |
| Dados / Integração  | HubSpot API                              |
| Infraestrutura      | Compatível com AWS, servidor local ou VM |

---

## Arquitetura e Etapas do Pipeline

```text
[HubSpot API] → Extração de dados (negócios + interações)
        ↓
[OpenAI API] → Vetorização semântica das frases (embeddings)
        ↓
[Clustering] → KMeans e HDBSCAN agrupam motivos semelhantes
        ↓
[GPT-4] → Geração automática de resumos dos motivos por cluster
        ↓
[Dashboards / CSV] → Visualizações, gráficos e insights acionáveis
```

---

## Estrutura de Diretórios

```
app/
├── config/
│   ├── config.py                # Configurações gerais do projeto
│   └── paths.py                 # Definição de caminhos base
├── core/
│   └── routes.py                # Rotas principais do Flask
├── pipeline/
│   ├── clusterizar.py           # Algoritmos de clusterização (KMeans e HDBSCAN)
│   ├── interpretar_clusters.py  # Interpretação dos clusters com GPT
│   └── preparar_dados_dashboard.py # Pipeline para preparar dados do dashboard
├── presentation/
│   └── plotar_status_por_cluster.py # Geração de dados de status por cluster
├── services/
│   ├── gerar_dados_hubspot.py   # Extração de dados da API do HubSpot
│   └── gerar_embeddings.py      # Geração de embeddings com OpenAI
├── static/                      # Arquivos estáticos (CSS, imagens)
├── templates/                   # Templates HTML para renderização no Flask
├── utils/
│   └── visualizar.py            # Visualização de clusters com TSNE
├── app.py                       # Inicialização do servidor Flask
├── main.py                      # Arquivo principal para execução do pipeline
├── requirements.txt             # Dependências do projeto
├── .env                         # Variáveis de ambiente (chaves de API)
├── report/                      # Relatórios gerados (HTML, gráficos)
├── data/                        # Dados intermediários (CSV)
└── outputs/                     # Resultados das análises (CSV)
```

---

## Autenticação

As APIs da OpenAI e HubSpot utilizam tokens privados. As chaves devem estar no arquivo `.env`. Exemplo:

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
HUBSPOT_TOKEN=pat-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

---

## Como Executar o Projeto

1. **Instalar Dependências**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configurar Variáveis de Ambiente**:
   - Adicione as chaves de API no arquivo `.env`.

3. **Executar o Pipeline**:
   ```bash
   python main.py
   ```

4. **Iniciar o Servidor Flask**:
   ```bash
   python app.py
   ```

5. **Acessar o Dashboard**:
   - Abra o navegador e acesse `http://127.0.0.1:5000`.

---

## Projeção de Esforço e Custo

| Etapa                                | Tempo estimado    |
| ------------------------------------ | ----------------- |
| Levantamento e validação dos dados   | 5 dias            |
| Desenvolvimento completo do pipeline | 10 dias           |
| Integração com HubSpot e testes      | 4 dias            |
| Interface e ajustes finais           | 4 dias            |
| **Total**                            | **23 dias úteis** |

> O custo da OpenAI gira em torno de **US\$ 0,035 por 1.000 tokens processados**. O uso prático dependerá da quantidade e extensão dos textos coletados via HubSpot.

---

## Retorno Esperado

* Clareza sobre motivadores reais de compra/perda.
* Otimização da copy e timing de abordagem.
* Redução do churn por meio de insights preditivos.
* Segmentação estratégica baseada em padrões semânticos.

---

## Status do Projeto

✅ MVP funcional finalizado  
✅ Dados reais extraídos via API do HubSpot  
✅ Pipeline completo testado localmente  
✅ Repositório público com documentação  

---

## Autor

**Erikson Rodrigues**  
[LinkedIn](https://www.linkedin.com/in/eriksonrds) • [GitHub](https://github.com/eriksonrds)  
Especialista em IA aplicada à inovação comercial, com experiência em integrações cloud, automações e soluções corporativas.

---

## Observações

Este projeto foi desenvolvido como **proposta técnica no processo seletivo da Logcomex**. Todos os dados foram simulados para fins de validação e demonstração.
