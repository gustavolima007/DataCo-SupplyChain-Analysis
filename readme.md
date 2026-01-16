# Supply Chain Operational KPIs - DataCo Analysis

Análise avançada de supply chain usando o dataset **DataCo SMART SUPPLY CHAIN FOR BIG DATA ANALYSIS**. O projeto foca na criação de **KPIs operacionais** para monitoramento de desempenho logístico, atrasos, lucratividade e eficiência, com tratamento de dados em Python e visualização estratégica em Power BI.

Ideal para demonstrar habilidades em análise de dados operacionais, modelagem de KPIs e apresentação de insights para diretoria/stakeholders.

## 🎯 Objetivo do Projeto

Extrair insights acionáveis de uma base de supply chain com ~180.000 registros, respondendo perguntas como:

- Qual a taxa real de entregas no prazo (OTD)?
- Quais regiões/categorias geram mais atrasos e perdas de lucro?
- Qual o impacto financeiro de atrasos e descontos?
- Como otimizar operações com base em tendências e previsões?

## Tecnologias Utilizadas

- **Python** → Limpeza, transformação e cálculo de métricas (Pandas, NumPy)
- **Power BI** → Modelagem de dados, DAX avançado, dashboards interativos e visualizações
- **Dataset**: [DataCo SMART SUPPLY CHAIN FOR BIG DATA ANALYSIS](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis) (~180k linhas)

## KPIs Criados

| KPI                         | Descrição                                  | Fórmula Principal (DAX/Exemplo)                       | Impacto Estratégico                       |
| --------------------------- | -------------------------------------------- | ------------------------------------------------------ | ------------------------------------------ |
| On-Time Delivery (OTD) Rate | % de entregas no prazo ou antecipadas        | DIVIDE(COUNTROWS(FILTER(... "On time")), Total Ordens) | Eficiência logística                     |
| Late Delivery Rate          | % de entregas atrasadas                      | % de "Late delivery"                                   | Identificação de gargalos                |
| Average Shipping Delay      | Dias médios de atraso em entregas atrasadas | AVERAGE([Days real] - [Days scheduled])                | Quantificação de problemas operacionais  |
| Profit per Order            | Lucro médio por pedido                      | AVERAGE([Order Profit Per Order])                      | Análise de rentabilidade                  |
| Average Order Value (AOV)   | Valor médio por pedido                      | SUM([Sales]) / COUNTROWS(Orders)                       | Segmentação de clientes e precificação |
| Product Profit Margin       | Margem de lucro por categoria/produto        | DIVIDE(SUM([Profit]), SUM([Sales]))                    | Priorização de portfólio de produtos    |
| Late Delivery Risk Score    | Pontuação média de risco de atraso        | AVERAGE([Late_delivery_risk])                          | Prevenção e alertas proativos            |

## Estrutura do Repositório

- `datasets/` → dados brutos: `tokenized_access_logs.csv` e `DataCoSupplyChainDataset.csv`
- `data/` → arquivos transformados gerados pela pipeline (`tokenized_access_logs_transformed.csv`, `DataCoSupplyChainDataset_transformed.csv`)
- `pipe/01-transform.py` → script Python responsável por normalizar datas, exibir shape/stats/amostras e salvar os dois CSVs formatados
- `power-bi/` → artefatos de dashboard e relatórios interativos (modelos `.pbix`, imagens etc.)

## Como rodar a transformação

1. Instale dependências em um ambiente virtual (recomendado):

```bash
python -m venv .venv
.venv/Scripts/activate    # Windows
.venv/bin/activate       # macOS/Linux
pip install pandas
```

2. Execute o pipeline principal:

```bash
python pipe/01-transform.py
```

O script:

- normaliza a coluna `Date` do `tokenized_access_logs.csv` para `DD/MM/AAAA`.
- converte `order date (DateOrders)` e `shipping date (DateOrders)` em `DataCoSupplyChainDataset.csv`.
- imprime shape, estatísticas e amostras das duas tabelas.
- salva os resultados limpos em `data/tokenized_access_logs_transformed.csv` e `data/DataCoSupplyChainDataset_transformed.csv`.

## Dados

- `tokenized_access_logs.csv` → logs de acesso de clientes, usado para analisar comportamento e sessões em departamentos e produtos.
- `DataCoSupplyChainDataset.csv` → pedidos com informações de shipping, lucros, regiões e KPIs operacionais detalhados. Lê-se com `encoding="latin-1"` por conter acentos.
