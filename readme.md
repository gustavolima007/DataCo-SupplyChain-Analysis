# Supply Chain Operational KPIs - DataCo Analysis

Análise avançada de supply chain usando o dataset **DataCo SMART SUPPLY CHAIN FOR BIG DATA ANALYSIS**. O projeto foca na criação de **KPIs operacionais** para monitoramento de desempenho logístico, atrasos, lucratividade e eficiência, com pré-processamento de dados em Python e visualização e transformação estratégica em Power BI.

Ideal para demonstrar habilidades em análise de dados operacionais, modelagem de KPIs e apresentação de insights para diretoria/stakeholders.

## 🎯 Objetivo do Projeto

Extrair insights acionáveis de uma base de supply chain com ~180.000 registros, respondendo perguntas como:

- Qual a taxa real de entregas no prazo (OTD)?
- Quais regiões/categorias geram mais atrasos e perdas de lucro?
- Qual o impacto financeiro de atrasos e descontos?
- Como otimizar operações com base em tendências e previsões?

## Tecnologias Utilizadas

- **Python (Pandas)** → Pré-processamento e limpeza inicial de tipos de dados.
- **Power BI (Linguagem M & DAX)** → Modelagem de dados, transformações avançadas, DAX, dashboards interativos e visualizações.
- **Dataset**: [DataCo SMART SUPPLY CHAIN FOR BIG DATA ANALYSIS](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis) (~180k linhas)

## KPIs Desenvolvidos no Power BI

Os seguintes KPIs foram modelados diretamente no Power BI utilizando DAX para permitir a análise dinâmica e interativa dos dados.

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

- `datasets/` → Dados brutos do DataCo (`tokenized_access_logs.csv` e `DataCoSupplyChainDataset.csv`). **Atenção:** os arquivos são modificados pelo script Python.
- `pipe/01-transform.py` → Script Python para correção de tipos de dados (datas e colunas financeiras) diretamente nos arquivos da pasta `datasets/`.
- `power-bi/` → Projeto do Power BI (`.pbip`) contendo o modelo de dados, transformações (Linguagem M) e o relatório visual.

## Como rodar o pré-processamento

O script Python serve para garantir que as colunas de data e valores financeiros sejam carregadas corretamente no Power BI, evitando erros de tipo.

1. Instale as dependências:

```bash
pip install pandas
```

2. Execute o pipeline de pré-processamento:

```bash
python pipe/01-transform.py
```

O script fará o seguinte:
- **Normaliza colunas de data** para o formato `datetime`.
- **Converte colunas financeiras** para o tipo `numeric`.
- **Sobrescreve os arquivos originais** em `datasets/DataCo_Smart_Supply/` com os tipos corrigidos.

Após a execução, os dados estão prontos para serem atualizados no Power BI, onde as transformações principais são realizadas.

## Dados

- `tokenized_access_logs.csv` → logs de acesso de clientes, usado para analisar comportamento e sessões em departamentos e produtos.
- `DataCoSupplyChainDataset.csv` → pedidos com informações de shipping, lucros, regiões e KPIs operacionais detalhados. Lê-se com `encoding="latin-1"` por conter acentos.
