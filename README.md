# E-Commerce Price Variation Pipeline

🚀 **Projeto de Engenharia de Dados End-to-End**

Análise de variações de preços em e-commerce usando o dataset Olist (Brazilian E-Commerce Public Dataset), implementando uma arquitetura Medallion (Raw → Bronze → Silver → Gold) com Python, pandas e formatos otimizados (Parquet).

---

## 📋 Visão Geral

| Item | Descrição |
|------|-----------|
| **Objetivo** | Extrair, transformar e agregar dados de e-commerce em KPIs prontos para BI |
| **Dataset** | Olist Brazilian E-Commerce (~100k pedidos, ~1M itens, 72 categorias) |
| **Período** | 2016-09 a 2018-10 |
| **Arquitetura** | Medallion (Raw → Bronze → Silver → Gold) |
| **Tecnologias** | Python 3.8+, pandas, pyarrow (Parquet), Docker (MinIO opcional) |
| **Tempo de Execução** | ~30 seg (amostra) / ~5-10 min (dataset completo) |

---

## 📂 Estrutura do Repositório

```
TrabalhoBigData/
├── docs/                              # 📚 Documentação completa
│   ├── DOCUMENTACAO_GERAL.md         # Documentação técnica detalhada (3.500+ linhas)
│   ├── confluence_export.md           # Pronto para importar no Confluence
│   └── confluence_template.md         # Template Confluence
├── src/                               # 🐍 Scripts Python
│   ├── ingestao.py                   # Etapa 1: Raw → Bronze (normalização)
│   ├── processamento.py               # Etapa 2: Bronze → Silver (transformação)
│   ├── gold.py                        # Etapa 3: Silver → Gold (KPIs)
│   ├── processamento_fix.py           # Versão otimizada (chunked reading)
│   └── gold_fix.py                    # Versão otimizada para datasets grandes
├── notebooks/                         # 📊 Jupyter Notebooks
│   └── 01_eda_olist.ipynb            # Análise Exploratória de Dados (EDA)
├── infra/                             # 🐳 Infraestrutura
│   └── docker-compose.yaml            # MinIO (S3-compatible storage, opcional)
├── datasets/                          # 📦 Dados de teste
│   ├── README.md                      # Guia de dados
│   └── sample_data/                   # Amostra para testes rápidos
│       ├── olist_orders_sample.csv
│       ├── olist_order_items_sample.csv
│       ├── olist_products_sample.csv
│       ├── olist_customers_sample.csv
│       └── olist_sellers_sample.csv
├── Datasets/                          # 🏗️ Data Lake (criado automaticamente)
│   ├── Source/                        # Dados brutos (Kaggle)
│   ├── Raw/                           # Cópia literal
│   ├── Bronze/                        # Normalizado (CSV)
│   ├── Silver/                        # Transformado (Parquet)
│   └── Gold/                          # KPIs (CSV)
├── diagrams/                          # 📐 Diagramas
│   └── architecture.mmd               # Diagrama Mermaid da arquitetura
├── requirements.txt                   # 📋 Dependências Python
└── README.md                          # Este arquivo
```

---

## 🚀 Início Rápido

### Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes)
- Git
- VS Code (opcional)

### 1️⃣ Clone e Configure

```powershell
# Clone o repositório
git clone https://github.com/HenriqueForin0905/TrabalhoBigData.git
cd TrabalhoBigData

# Abra no VS Code (opcional)
code .

# Crie virtual environment
python -m venv venv

# Ative (Windows)
.\venv\Scripts\Activate.ps1
# OU (macOS/Linux)
source venv/bin/activate

# Instale dependências
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 2️⃣ Teste Rápido (30 segundos com amostra)

```powershell
# Copie dados de amostra para Source
cp .\datasets\sample_data\*.csv .\Datasets\Source\

# Execute o pipeline completo
python .\src\ingestao.py        # Raw → Bronze
python .\src\processamento.py   # Bronze → Silver
python .\src\gold.py             # Silver → Gold

# Verifique resultados
ls .\Datasets\Gold\
```

**Resultado esperado:**
- `avg_price_by_category.csv` - Preço médio por categoria
- `price_variation_by_month.csv` - Variação mensal

### 3️⃣ Análise Completa (Dados Kaggle)

```powershell
# Baixe o dataset Olist do Kaggle
# https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

# Copie os CSVs para Source
cp .\datasets\full_data\olist*.csv .\Datasets\Source\

# Execute o pipeline
python .\src\ingestao.py
python .\src\processamento.py
python .\src\gold.py

# Tempo total: ~5-10 minutos
```

### 4️⃣ Análise Exploratória (EDA)

```powershell
# Abra Jupyter Notebook
jupyter notebook notebooks/01_eda_olist.ipynb

# Explore os dados:
# - Estatísticas descritivas
# - Distribuições de preços
# - Análise temporal
# - Visualizações
# - Insights principais
```

---

## 📊 Pipeline Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    PIPELINE DE DADOS                          │
└──────────────────────────────────────────────────────────────┘

Etapa 1: INGESTÃO (ingestao.py)
  Source CSV → Read → Raw (cópia literal) → Bronze (normalizado)
  ✓ Normaliza nomes de colunas (snake_case)
  ✓ Preserva dados para auditoria

Etapa 2: PROCESSAMENTO (processamento.py)
  Bronze CSV → Load → Transformação → Silver (Parquet)
  ✓ Padroniza tipos de dados
  ✓ Converte datas para datetime
  ✓ Trata nulos (numeric → 0, text → NaN, date → NaT)
  ✓ Comprime com Parquet (70-90% menos espaço)

Etapa 3: AGREGAÇÃO (gold.py)
  Silver Parquet → Load → Cálculos → Gold (CSV)
  ✓ avg_price_by_category (preço médio por categoria)
  ✓ price_variation_by_month (variação mensal)
  ✓ Pronto para BI tools

┌──────────────────────────────────────────────────────────────┐
│  Power BI / Metabase / Tableau / Excel (BI Tools)            │
└──────────────────────────────────────────────────────────────┘
```

---

## 🔑 KPIs Gerados

### avg_price_by_category.csv

```csv
product_category_name,avg_price
telefonica,150.45
electronics,120.30
esportes,98.75
...
```

### price_variation_by_month.csv

```csv
month,avg_price,min_price,max_price
2016-09,100.00,10.00,5000.00
2016-10,105.50,12.00,4800.00
...
```

---

## 🛠️ Integração com BI Tools

### Power BI

1. Abra Power BI Desktop
2. **Home** → **Get Data** → **Folder**
3. Aponte para `Datasets/Gold/`
4. **Load** e crie visualizações

### Metabase

1. Inicie Metabase (Docker ou local)
2. **Admin Settings** → **Databases** → **Add Database**
3. Tipo: **File** → Aponte para `Datasets/Gold/`
4. **Browse** e crie dashboards

### Google Sheets / Excel

1. **File** → **Open** → Selecione CSV em `Gold/`
2. Crie gráficos e análises

---

## 📈 Dados & Estatísticas

| Métrica | Valor |
|---------|-------|
| **Total de Pedidos** | ~100.000 |
| **Total de Itens** | ~1.000.000 |
| **Categorias Únicas** | ~72 |
| **Vendedores** | ~3.500 |
| **Clientes** | ~100.000 |
| **Período** | 2016-09 a 2018-10 (775 dias) |
| **Preço Médio** | ~R$ 120,77 |
| **Preço Range** | R$ 0,85 - R$ 13.664,00 |

Para detalhes completos, veja `datasets/README.md`

---

## 📚 Documentação

| Arquivo | Conteúdo |
|---------|----------|
| **DOCUMENTACAO_GERAL.md** | Documentação técnica completa (3.500+ linhas): arquitetura, decisões técnicas, troubleshooting, limitações |
| **confluence_export.md** | Versão formatada para Confluence (pronta para importar) |
| **notebooks/01_eda_olist.ipynb** | Análise exploratória com visualizações e insights |
| **datasets/README.md** | Guia de dados, esquema, estatísticas |

---

## 🔧 Comandos Úteis

### Executar Pipeline Completo

```powershell
python .\src\ingestao.py && python .\src\processamento.py && python .\src\gold.py
```

### Verificar Dados em Cada Camada

```powershell
# Raw
ls .\Datasets\Raw\ | Select-Object Name, Length

# Bronze
ls .\Datasets\Bronze\ | Select-Object Name, Length

# Silver
ls .\Datasets\Silver\ | Select-Object Name, Length

# Gold (KPIs)
gc .\Datasets\Gold\avg_price_by_category.csv | head -20
```

### Validar Instalação

```powershell
python -c "import pandas; import pyarrow; print('✅ OK')"
```

### Usar com MinIO (Opcional)

```powershell
# Inicie MinIO com Docker
docker-compose -f .\infra\docker-compose.yaml up -d

# Acesse console
# URL: http://localhost:9001
# User: minioadmin
# Password: minioadmin

# Pare o serviço
docker-compose -f .\infra\docker-compose.yaml down
```

---

## ⚙️ Configuração Avançada

### Ajustar Diretórios

```powershell
# Usar diretórios customizados
python .\src\ingestao.py --source "C:\path\to\data" --datasets-dir "C:\path\to\Datasets"

python .\src\processamento.py --datasets-dir "C:\path\to\Datasets"

python .\src\gold.py --datasets-dir "C:\path\to\Datasets"
```

### Agendar Execução Automática (Windows Task Scheduler)

1. Crie arquivo `run_pipeline.bat`:
   ```batch
   @echo off
   cd C:\Users\...\TrabalhoBigData
   .\venv\Scripts\Activate.ps1
   python .\src\ingestao.py && python .\src\processamento.py && python .\src\gold.py
   echo Pipeline executed at %date% %time% >> pipeline.log
   ```

2. Abra Task Scheduler e agende para rodar diariamente

### Escalar para PySpark

Para datasets > 1GB, migre para PySpark:

```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("Pipeline").getOrCreate()
df = spark.read.csv("source.csv")
# Processamento distribuído
```

---

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'pandas'"

```powershell
pip install pandas>=1.3
```

### Erro: "No such file or directory: 'Datasets/Source'"

```powershell
mkdir .\Datasets\Source
# Copie os CSVs aqui
```

### Erro: "OutOfMemory" em datasets grandes

```powershell
# Use versão otimizada
python .\src\processamento_fix.py
```

Para mais soluções, veja seção "Troubleshooting" em `docs/DOCUMENTACAO_GERAL.md`

---

## 🎯 Próximos Passos

- [ ] Baixe dados completos do Kaggle
- [ ] Execute pipeline completo
- [ ] Crie dashboard em Power BI ou Metabase
- [ ] Estenda com KPIs customizados
- [ ] Implemente orchestração (Airflow)
- [ ] Configure backup/DR

---

## 📖 Referências

- **Dataset Olist:** https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
- **Pandas Docs:** https://pandas.pydata.org/docs/
- **Parquet Format:** https://parquet.apache.org/
- **Medallion Architecture:** [Delta Lake](https://delta.io/)

---

## 📝 Licença

Este projeto está licenciado sob MIT License. O dataset Olist é de domínio público.

---

**Última Atualização:** Dezembro 2025  
**Mantido por:** Projeto TrabalhoBigData  
**Contato:** [GitHub Issues](https://github.com/HenriqueForin0905/TrabalhoBigData/issues)
