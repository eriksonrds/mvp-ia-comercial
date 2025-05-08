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
5. **Interpretação automática dos clusters** com GPT-4o.
6. **Geração de dashboards interativos e relatórios CSV.**

---

## Tecnologias Utilizadas

| Categoria           | Ferramentas / Tecnologias                |
| ------------------- | ---------------------------------------- |
| Linguagem principal | Python                                   |
| IA e NLP            | OpenAI Embeddings, GPT-4o                |
| Clustering          | Scikit-learn (KMeans), HDBSCAN           |
| Visualização        | Matplotlib, Seaborn, TSNE                |
| Web (opcional)      | Flask (Interface interativa)             |
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
[GPT-4o] → Geração automática de resumos dos motivos por cluster
        ↓
[Dashboards / CSV] → Visualizações, gráficos e insights acionáveis
```

---

## Estrutura de Diretórios

```
 src/
 ├── gerar_dados_hubspot.py
 ├── gerar_embeddings.py
 ├── clusterizar.py
 ├── visualizar.py
 └── interpretar_clusters.py

 data/
 ├── interacoes_hubspot.csv
 ├── interacoes_com_embeddings.csv
 └── interacoes_clusterizadas.csv

 outputs/
 ├── tsne_kmeans.png
 ├── tsne_hdbscan.png
 ├── resumos_kmeans.csv
 └── resumos_hdbscan.csv

main.py
requirements.txt
.env (não subir para o GitHub)
README.md
```

---

## Autenticação

A API da OpenAI e a API do HubSpot exigem tokens privados para uso. As chaves são lidas via arquivo `.env`. Exemplo de configuração:

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
HUBSPOT_PRIVATE_TOKEN=pat-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

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
