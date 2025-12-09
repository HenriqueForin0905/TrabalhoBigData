# Confluence - Projeto: Variação de Preços E-Commerce

**Visão Geral**: O projeto constrói um pipeline em camadas (Raw → Bronze → Silver → Gold) para analisar variações de preço no dataset Olist.

**Objetivos**
- Demonstrar engenharia de dados end-to-end
- Transformar dados brutos em métricas acionáveis
- Produzir visualizações para apoiar decisões

**Arquitetura**

```mermaid
graph LR
  A[Source CSVs] --> B[Raw]
  B --> C[Bronze]
  C --> D[Silver]
  D --> E[Gold (KPIs)]
  E --> F[BI / Dashboard]
```

**Camadas**
- Raw: cópia dos CSVs originais
- Bronze: limpeza leve, padronização de colunas
- Silver: tipos padronizados, joins, tratamento de nulos
- Gold: tabelas prontas para consumo com KPIs

**Guia de Execução**

1. Clonar repositório
2. Instalar dependências: `pip install -r requirements.txt`
3. Colocar CSVs em `Datasets/Source`
4. Executar ingestão: `python src/ingestao.py`
5. Processar Bronze → Silver: `python src/processamento.py`
6. Gerar Gold: `python src/gold.py`

**Dicionário de Dados (exemplo)**
- `orders.csv`: order_id, customer_id, order_status, order_approved_at
- `order_items.csv`: order_id, product_id, price, freight_value
- `products.csv`: product_id, product_category_name

**Métricas Principais (Gold)**
- `avg_price_by_category`
- `price_variation_by_month`
- `ticket_medio_por_mes`

**Próximos passos**
- Integrar MinIO e apontar pipeline para S3
- Criar alerta de mudança de preço (threshold)
- Construir dashboard no Metabase ou Power BI
