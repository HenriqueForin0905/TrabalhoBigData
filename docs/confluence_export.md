# Documentação Geral - E-Commerce Price Variation Pipeline

{toc}

## Descrição do Problema

h3. Contexto

O projeto aborda a **análise de variações de preços em e-commerce** utilizando dados históricos do setor de vendas online brasileiro. O dataset Olist (Brazilian E-Commerce Public Dataset) contém informações reais de transações de um marketplace multi-vendedor.

h3. Desafios

* **Volume de Dados**: Millões de registros de pedidos, produtos, vendedores e preços requerem processamento eficiente
* **Heterogeneidade de Dados**: Dados brutos com inconsistências de nomenclatura, tipos e valores faltantes
* **Análise Temporal**: Identificar padrões de preço ao longo do tempo é complexo sem estruturação adequada
* **Escalabilidade**: A solução deve permitir adicionar novas fontes de dados sem refatoração completa

h3. Problema Central

{quote}Como estruturar e processar dados de e-commerce para extrair insights sobre variação de preços em categorias de produtos e períodos temporais, permitindo que ferramentas de BI (Business Intelligence) façam análises autoatendidas?{quote}

---

## Objetivos do Sistema

h3. Objetivos Primários

# Ingestão Automatizada: Carregar dados de múltiplas fontes CSV com normalização básica
# Processamento em Camadas: Implementar arquitetura de data lake com raw → bronze → silver → gold
# Transformação de Qualidade: Padronizar tipos de dados, tratar nulos e normalizar nomenclaturas
# Geração de KPIs: Produzir métricas prontas para visualização (preço médio por categoria, variação mensal)
# Integração com BI: Exportar dados estruturados (Parquet/CSV) para ferramentas como Power BI ou Metabase

h3. Objetivos Secundários

* Fornecer rastreabilidade completa (raw → gold)
* Permitir reprocessamento incremental
* Documentar esquemas de dados em cada camada
* Facilitar manutenção e extensão do pipeline

h3. Justificativa Técnica

A arquitetura em camadas (Medallion Architecture) oferece:
* **Isolamento**: Cada etapa tem responsabilidade única
* **Rastreabilidade**: Dados brutos preservados para auditoria
* **Flexibilidade**: Novas transformações adicionadas sem afetar existentes
* **Performance**: Formatos otimizados (Parquet) em camadas superiores
* **Governança**: Controle explícito sobre qualidade dos dados em cada nível

---

## Escopo da Solução

h3. Incluído

| Item | Descrição |
|------|-----------|
| **Ingestão (Raw)** | Leitura de CSVs da pasta Source; cópia sem alteração para Raw |
| **Normalização (Bronze)** | Limpeza de nomes de colunas (snake_case, alfanuméricos) |
| **Processamento (Silver)** | Conversão de tipos, tratamento de nulos, validação básica |
| **Agregação (Gold)** | KPIs: preço médio por categoria, variação mensal de preços |
| **Exportação** | Formatos CSV (Gold) e Parquet (Silver) para BI tools |
| **Logging** | Rastreamento de execução e erros em cada etapa |
| **Infraestrutura Opcional** | Docker Compose com MinIO para armazenamento distribuído |

h3. Não Incluído

| Item | Motivo |
|------|--------|
| **Orchestração (Airflow, Dagster)** | Escopo simplificado; execução manual ou cron jobs |
| **Data Warehouse (Snowflake, BigQuery)** | Foco em estrutura local; extensível a cloud |
| **ML/Previsão** | Foco em análise descritiva; não preditiva |
| **API REST** | Dados consumidos diretamente de arquivos |
| **Testes Automatizados** | Escopo mínimo; testes manuais esperados |
| **CI/CD Pipeline** | Não configurado; pode ser adicionado |
| **Replicação de Dados** | Operação unitária, não contínua |
| **Data Quality Checks Complexos** | Validações básicas apenas |

---

## Arquitetura Completa

 1. Arquitetura Geral (Medallion Architecture)

{code:text}
┌──────────────────────────────────────────────────────────────────┐
│                     E-COMMERCE PRICE VARIATION PIPELINE            │
└──────────────────────────────────────────────────────────────────┘

┌─────────────┐     ┌──────────────────┐     ┌──────────────────┐
│   SOURCE    │     │      RAW LAYER   │     │   BRONZE LAYER   │
│  (External) │────▶│ (Dados Brutos)   │────▶│ (Normalizado)    │
└─────────────┘     └──────────────────┘     └──────────────────┘
     ▲                       │                        │
     │                       │                        │
  CSV Files             CSV Format             CSV Format
  (Olist Dataset)       No Changes            Column Names:
                        Preservação            - snake_case
                        Completa              - only alphanumeric
                                             - normalized spacing

        ┌──────────────────┐     ┌──────────────────┐
        │  SILVER LAYER    │     │   GOLD LAYER     │
        │ (Processado)     │────▶│ (KPIs/Analytics) │
        └──────────────────┘     └──────────────────┘
             │                           │
        Parquet Format              CSV Format
        - Type Parsing              - avg_price_by_category
        - Null Handling            - price_variation_by_month
        - Date Conversion          (Ready for BI)
{code}

2. Estrutura de Diretórios

{code:text}
TrabalhoBigData/
├── src/                              # Scripts Python
│   ├── ingestao.py                  # Raw → Bronze
│   ├── processamento.py              # Bronze → Silver
│   ├── gold.py                       # Silver → Gold
│   ├── processamento_fix.py          # Versão alternativa
│   ├── gold_fix.py                   # Versão alternativa
│   └── __pycache__/                 # Cache Python
├── Datasets/                         # Data Lake
│   ├── Source/                      # Dados externos (Olist)
│   ├── Raw/                         # Cópia literal
│   ├── Bronze/                      # Normalizado
│   ├── Silver/                      # Processado (Parquet)
│   └── Gold/                        # KPIs (CSV)
├── infra/
│   └── docker-compose.yaml          # MinIO (opcional)
├── docs/
│   ├── DOCUMENTACAO_GERAL.md        # Documentação completa
│   └── confluence_template.md        # Template Confluence
├── diagrams/
│   └── architecture.mmd              # Diagrama Mermaid
├── requirements.txt                  # Dependências Python
└── README.md                         # Quick start
{code}

h3. 3. Fluxo de Dados Detalhado

h4. Etapa 1: Ingestão (ingestao.py)

{code:text}
Input: Datasets/Source/*.csv (Olist Dataset)
  ├─ olist_customers_dataset.csv
  ├─ olist_orders_dataset.csv
  ├─ olist_order_items_dataset.csv
  ├─ olist_products_dataset.csv
  └─ olist_sellers_dataset.csv

Processing:
  1. Read CSV file → pandas DataFrame
  2. Save unmodified → Datasets/Raw/
  3. Normalize column names:
     - Strip whitespace
     - Convert to lowercase
     - Replace spaces with underscores
     - Remove special characters (keep only alphanumeric + _)
     - Remove leading/trailing underscores
  4. Save normalized → Datasets/Bronze/

Output: Datasets/Bronze/*.csv (Normalized CSVs)
{code}

**Função Principal: `ingest_csv()`**

{code:python}
# Normalização de colunas
def _norm_column(col: str) -> str:
    col = str(col).strip().lower()
    col = re.sub(r"\s+", "_", col)                    # espaços → _
    col = re.sub(r"[^0-9a-zA-Z_]+", "_", col)       # caracteres especiais
    col = re.sub(r"_+", "_", col)                     # múltiplos _ → _
    return col.strip("_")
{code}

h4. Etapa 2: Processamento (processamento.py)

{code:text}
Input: Datasets/Bronze/*.csv (Normalized CSVs)

Processing:
  1. Load each Bronze CSV
  2. Standardize column names (lowercase, trim)
  3. Parse dates:
     - Detecta colunas com 'date', '_dt', '_date'
     - Converte para datetime (coerce errors → NaT)
  4. Fill nulls for numeric columns:
     - Select numeric columns
     - Replace NaN with 0
  5. Save to Parquet (compression, efficient storage)

Output: Datasets/Silver/*.parquet (Processed Data)
{code}

h4. Etapa 3: Agregação Gold (gold.py)

{code:text}
Input: Datasets/Silver/*.parquet (Processed Data)

Processing:
  1. Load all Silver Parquet files as DataFrames
  2. Generate KPI 1: avg_price_by_category
     - Join order_items (price) + products (category)
     - GROUP BY product_category_name
     - Calculate MEAN(price)
     - Output: category | avg_price
     
  3. Generate KPI 2: price_variation_over_time
     - Extract order_approved_at month
     - GROUP BY month
     - Calculate MEAN, MIN, MAX of price
     - Output: month | avg_price | min_price | max_price

Output: Datasets/Gold/*.csv (Ready for BI)
{code}

---

## Ferramentas e Tecnologias

h3. Linguagem & Runtime

| Tecnologia | Versão | Propósito |
|-----------|--------|----------|
| **Python** | 3.8+ | Linguagem principal para processamento |
| **pip** | Latest | Gerenciador de pacotes Python |

h3. Dependências de Processamento

| Biblioteca | Versão | Propósito |
|-----------|--------|----------|
| **pandas** | ≥1.3 | Manipulação de DataFrames, leitura/escrita CSV |
| **pyarrow** | ≥8.0 | Engine para Parquet, integração com pandas |
| **fastparquet** | ≥0.8 | Engine alternativa para Parquet |
| **pyspark** | ≥3.2 | Opcional: processamento distribuído em escala |

h3. Armazenamento (Opcional)

| Ferramenta | Versão | Propósito |
|-----------|--------|----------|
| **MinIO** | latest | S3-compatible object storage (Docker) |
| **Docker** | Latest | Containerização (docker-compose) |

h3. Ferramentas de BI (Downstream)

* **Power BI**: Importação de CSV/Parquet do Gold
* **Metabase**: Query sobre CSVs em Gold
* **Tableau**: Integração com dados estruturados
* **Google Sheets / Excel**: Importação direta de CSVs

---

## Decisões Técnicas

h3. 1. Arquitetura Medallion (Raw → Bronze → Silver → Gold)

h4. Alternativas Consideradas

* ❌ Pipeline único (Raw → Gold): Perda de rastreabilidade, difícil auditoria
* ❌ Data Warehouse centralizado (Snowflake): Custo $$, overkill para escopo inicial
* ✅ **Medallion Local**: Simplicidade, rastreabilidade, extensível

h4. Trade-offs

* ✅ Preserva dados brutos para reprocessamento
* ✅ Cada camada tem responsabilidade clara
* ❌ Uso de disco duplicado (Raw + Bronze similar)
* ❌ Processamento sequencial (não paralelo)

h3. 2. Formatos de Arquivo por Camada

| Camada | Formato | Justificativa |
|--------|---------|---------------|
| **Raw** | CSV | Preservação literal; simples, universal |
| **Bronze** | CSV | Compatível com ferramentas padrão |
| **Silver** | **Parquet** | Compressão, tipos nativos, eficiência |
| **Gold** | CSV | Universalidade para BI tools |

h4. Por que Parquet em Silver?

* Compressão automática (reduz 70-90% do tamanho)
* Tipos de dados preservados (date, int, float nativo)
* Query push-down (leitura seletiva de colunas)
* Standard em data lakes (Spark, Hadoop, etc.)

h3. 3. Tratamento de Nulos em Silver

h4. Abordagem

* Colunas numéricas: fill NaN com 0
* Colunas texto: deixar NaN (NULL)
* Datas: coerce invalid → NaT

h4. Justificativa

* 0 é seguro para agregações (SUM, AVG)
* NaT preserva semântica de dados faltantes
* Evita correlações falsas

h4. Limitação

Nem sempre 0 é apropriado (ex: preço 0 ≠ nulo)

h3. 4. KPIs em Gold

h4. Gerados

1. **avg_price_by_category**
   ```
   product_category_name | avg_price
   electronics           | 150.45
   books                 | 25.30
   ```

2. **price_variation_by_month**
   ```
   month  | avg_price | min_price | max_price
   2016-09 | 100.00   | 10.00     | 5000.00
   2016-10 | 105.50   | 15.00     | 4500.00
   ```

---

## Guia de Execução

h3. Pré-requisitos

* **Sistema Operacional**: Windows / macOS / Linux
* **Python**: 3.8+ instalado
* **pip**: Gerenciador de pacotes Python
* **Git**: Para clonar repositório
* **VS Code** (Opcional): Para editar/debugar código

h3. 1. Clone o Repositório

{code:powershell}
# Clone
git clone https://github.com/HenriqueForin0905/TrabalhoBigData.git

# Entre no diretório
cd TrabalhoBigData

# Abra no VS Code (opcional)
code .
{code}

h3. 2. Configure o Ambiente

{code:powershell}
# Crie um Virtual Environment (recomendado)
python -m venv venv

# Ative o Virtual Environment
# Windows:
.\venv\Scripts\Activate.ps1

# Instale dependências
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
{code}

h3. 3. Prepare os Dados Fonte (Source)

{code:powershell}
# Opção 1: Download manual
# Visite: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
# Extraia em: Datasets/Source/

# Opção 2: Criar estrutura de exemplo
mkdir -p Datasets/Source
# Coloque CSVs aqui: olist_*.csv
{code}

h3. 4. Execute o Pipeline Completo

h4. Etapa 1: Ingestão (Raw → Bronze)

{code:powershell}
python .\src\ingestao.py
{code}

h4. Etapa 2: Processamento (Bronze → Silver)

{code:powershell}
python .\src\processamento.py
{code}

h4. Etapa 3: Agregação (Silver → Gold)

{code:powershell}
python .\src\gold.py
{code}

h3. 5. Integre com BI Tool

h4. Power BI

# Abra Power BI Desktop
# Home → Get Data → Folder
# Aponte para `Datasets/Gold/`
# Selecione arquivos CSV
# Transform → Load
# Crie visualizações

h4. Metabase

# Inicie Metabase (Docker ou local)
# Admin Settings → Databases
# Add Database → File
# Aponte para `Datasets/Gold/`
# Browse → Create Dashboard

h3. 6. Automação (Cron/Task Scheduler)

h4. Windows Task Scheduler

{code:powershell}
# Crie arquivo batch: run_pipeline.bat
@echo off
cd C:\Users\Administrador\TrabalhoBigData
.\venv\Scripts\Activate.ps1
python .\src\ingestao.py
python .\src\processamento.py
python .\src\gold.py
echo Pipeline executed at %date% %time% >> pipeline.log
{code}

Agenda no Task Scheduler:
* Ação: Executar `run_pipeline.bat`
* Frequência: Diária às 02:00

---

## Guia de Dependências

h3. Versões Mínimas

{code}
Python                          3.8+
pandas                          1.3+
pyarrow (Parquet)              8.0+
fastparquet (Parquet alt.)     0.8+
pyspark (Opcional)             3.2+
{code}

h3. Instalação Detalhada

{code:powershell}
# 1. Upgrade pip
python -m pip install --upgrade pip

# 2. Instale requirements
pip install -r requirements.txt

# 3. Verifique versões
pip show pandas pyarrow fastparquet

# 4. (Opcional) Instale PySpark para distribuição
pip install pyspark==3.2.0
{code}

h3. MinIO (Opcional) - Docker Setup

{code:powershell}
# Inicie MinIO
docker-compose -f .\infra\docker-compose.yaml up -d

# Acesse console
# URL: http://localhost:9001
# User: minioadmin
# Password: minioadmin

# Parar serviço
docker-compose -f .\infra\docker-compose.yaml down
{code}

---

## Descrição dos Dados

h3. Origem dos Dados

* **Fonte**: Olist Brazilian E-Commerce Public Dataset
* **URL**: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
* **Cobertura**: Pedidos de 2016-09 a 2018-10
* **Registros**: ~100k pedidos, ~1M linhas totais
* **Tamanho**: ~50-100 MB (dados brutos)

h3. Tabelas/Datasets Principais

h4. 1. **olist_orders_dataset.csv**

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `order_id` | String | Identificador único do pedido |
| `customer_id` | String | ID do cliente |
| `order_status` | String | Status: delivered, cancelled, etc. |
| `order_purchase_timestamp` | DateTime | Quando o cliente fez a compra |
| `order_approved_at` | DateTime | Quando a compra foi aprovada |
| `order_delivered_carrier_date` | DateTime | Entrega pela transportadora |
| `order_delivered_customer_date` | DateTime | Entrega ao cliente |
| `order_estimated_delivery_date` | DateTime | Estimativa de entrega |

h4. 2. **olist_order_items_dataset.csv**

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `order_id` | String | FK para orders |
| `order_item_id` | Int | Sequência do item no pedido |
| `product_id` | String | FK para products |
| `seller_id` | String | FK para sellers |
| `shipping_limit_date` | DateTime | Limite para envio |
| `price` | Float | Preço unitário do produto |
| `freight_value` | Float | Custo do frete |

h4. 3. **olist_products_dataset.csv**

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `product_id` | String | Identificador único |
| `product_category_name` | String | Categoria do produto |
| `product_name_lenght` | Int | Comprimento do nome |
| `product_description_lenght` | Int | Comprimento da descrição |
| `product_photos_qty` | Int | Número de fotos |
| `product_weight_g` | Float | Peso em gramas |
| `product_length_cm` | Float | Comprimento em cm |
| `product_height_cm` | Float | Altura em cm |
| `product_width_cm` | Float | Largura em cm |

h3. Estatísticas do Dataset

| Métrica | Valor |
|---------|-------|
| Total de Pedidos | ~100,000 |
| Total de Itens | ~1,000,000 |
| Período | 2016-09 a 2018-10 |
| Categorias Únicas | ~70 |
| Vendedores | ~3,500 |
| Clientes | ~100,000 |
| Preço Médio | ~120 BRL |
| Preço Mín/Máx | 0.85 / 13,664 BRL |

---

## Pontos de Falha e Limitações

h3. Falhas Operacionais

h4. 1. Arquivo Source Não Encontrado

{quote}
WARNING: Source file not found: Datasets/Source/olist_customers_dataset.csv
{quote}

**Solução**:
* ✅ Verificar se arquivos estão em `Datasets/Source/`
* ✅ Usar argumentos `--source` e `--datasets-dir`

h4. 2. Erro de Memória (OutOfMemory)

{quote}
MemoryError: Unable to allocate XXX MB
{quote}

**Solução**:
* Usar `pd.read_csv(chunksize=10000)` para arquivos > 1GB
* Migrar para PySpark (processamento distribuído)
* Aumentar RAM da máquina

h3. Limitações Arquiteturais

h4. 1. Processamento Sequencial (Não Paralelo)

| Aspecto | Limitação |
|--------|-----------|
| **Velocidade** | Etapas executadas em série (Raw → Bronze → Silver → Gold) |
| **Escalabilidade** | Dataset > 1GB pode ser lento em máquinas com <8GB RAM |
| **CPU** | Não aproveita múltiplos cores/CPUs |

**Mitigação**: Usar PySpark para paralelismo

h4. 2. Sem Orchestração/Scheduling

* Execução manual
* Sem retry automático em caso de falha
* Sem dependências entre tarefas

**Solução**:
* ✅ Apache Airflow: DAGs, retry, monitoring
* ✅ Prefect: Cloud-native, UI intuitiva
* ✅ Cron/Task Scheduler: Simples para rotinas

h4. 3. Sem Data Quality Checks Complexos

**Checagens Atuais**:
* ✓ Arquivo existe?
* ✓ Pode ler CSV?
* ✓ Pode escrever?

**Checagens Ausentes**:
* ✗ Número de linhas esperado?
* ✗ Valores em range válido (preço > 0)?
* ✗ Chaves estrangeiras válidas?
* ✗ Outliers detectados?

h3. Recomendações de Melhoria

| Prioridade | Item | Esforço | ROI |
|-----------|------|--------|-----|
| **P0** | Data Quality Framework | Alto | Alto |
| **P0** | Orchestração (Airflow) | Alto | Alto |
| **P1** | Versionamento de Dados | Médio | Médio |
| **P1** | Testes Automatizados | Médio | Médio |
| **P2** | KPIs Customizados | Médio | Médio |
| **P2** | Backup/DR | Médio | Alto |
| **P3** | API REST | Alto | Baixo |
| **P3** | Data Catalog | Alto | Médio |

---

## Troubleshooting

h3. Problema: "ModuleNotFoundError: No module named 'pandas'"

{code:powershell}
# Solução
pip install pandas>=1.3
{code}

h3. Problema: "No such file or directory: 'Datasets/Source'"

{code:powershell}
# Solução
mkdir Datasets\Source
# Copie CSVs para este diretório
{code}

h3. Problema: Parquet files unreadable

{code:powershell}
# Solução
pip install --upgrade pyarrow fastparquet
{code}

h3. Problema: OutOfMemory em datasets grandes

{code:powershell}
# Use chunked reading
python src/processamento_fix.py  # versão otimizada
{code}

---

## Conclusão

Este projeto implementa uma solução **end-to-end** de data lake com arquitetura medallion, processamento com Python/pandas e integração com ferramentas de BI.

h3. Pontos Fortes

* ✅ Arquitetura clara e escalável
* ✅ Rastreabilidade completa (Raw → Gold)
* ✅ Formatos otimizados (Parquet)
* ✅ Código documentado e modular

h3. Áreas de Melhoria

* ⚠️ Sem orchestração automática
* ⚠️ Validações de qualidade limitadas
* ⚠️ Sem backup/DR
* ⚠️ KPIs genéricos

h3. Próximos Passos

# Validar com dados reais da empresa
# Implementar Airflow para agendamento
# Adicionar data quality checks
# Estender com KPIs de negócio específicos
# Migrar para PySpark para escala

---

*Última Atualização: Dezembro 2025*
*Mantido por: Projeto TrabalhoBigData*
