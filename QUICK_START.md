# Quick Reference - Guia de Referência Rápida

## Comandos Essenciais

### Setup Inicial

```powershell
# Clone
git clone https://github.com/HenriqueForin0905/TrabalhoBigData.git
cd TrabalhoBigData

# Virtual Environment
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Teste Rápido (30s)

```powershell
# Copiar dados de amostra
cp .\datasets\sample_data\*.csv .\Datasets\Source\

# Executar pipeline
python .\src\ingestao.py && python .\src\processamento.py && python .\src\gold.py

# Ver resultados
cat .\Datasets\Gold\avg_price_by_category.csv
```

### Análise Completa

```powershell
# Baixar do Kaggle e copiar para Source
# https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

# Executar pipeline
python .\src\ingestao.py && python .\src\processamento.py && python .\src\gold.py

# Abrir Jupyter
jupyter notebook notebooks/01_eda_olist.ipynb
```

---

##  Estrutura do Data Lake

```
Datasets/
├── Source/          → Dados brutos do Kaggle
├── Raw/             → Cópia literal (preservação)
├── Bronze/          → Colunas normalizadas (CSV)
├── Silver/          → Tipos padronizados (Parquet)
└── Gold/            → KPIs prontos para BI (CSV)
```

---

##  KPIs Gerados

### avg_price_by_category.csv
```csv
product_category_name,avg_price
telefonica,150.45
```

### price_variation_by_month.csv
```csv
month,avg_price,min_price,max_price
2016-09,100.00,10.00,5000.00
```

---

##  Docker/MinIO

```powershell
# Iniciar
docker-compose -f .\infra\docker-compose.yaml up -d

# Acessar console
# http://localhost:9001 (minioadmin/minioadmin)

# Parar
docker-compose down
```

---

##  Documentação Principal

| Arquivo | Para Quem | Conteúdo |
|---------|-----------|----------|
| **README.md** | Todos | Visão geral, início rápido |
| **DOCUMENTACAO_GERAL.md** | Técnicos | Arquitetura, decisões, troubleshooting |
| **src/README.md** | Desenvolvedores | Explicação de cada script |
| **infra/README.md** | DevOps | Docker, MinIO, Terraform, K8s |
| **datasets/README.md** | Data Analysts | Dicionário, estatísticas, esquema |
| **notebooks/01_eda_olist.ipynb** | Exploradores | EDA com gráficos e insights |

---

## Troubleshooting Rápido

### Erro: "ModuleNotFoundError: pandas"
```powershell
pip install pandas pyarrow
```

### Erro: "Datasets/Source não existe"
```powershell
mkdir .\Datasets\Source
cp .\datasets\sample_data\*.csv .\Datasets\Source\
```

### OutOfMemory
```powershell
# Use versão otimizada
python .\src\processamento_fix.py
python .\src\gold_fix.py
```

### Parquet erro
```powershell
pip install --upgrade pyarrow fastparquet
```

---

##  Integração BI

### Power BI
- Get Data → Folder → `Datasets/Gold/` → Load

### Metabase
- Admin → Databases → File → `Datasets/Gold/`

### Excel/Google Sheets
- File → Open → CSV em `Gold/`

---

##  Estatísticas Dataset

| Métrica | Valor |
|---------|-------|
| Pedidos | ~100.000 |
| Itens | ~1.000.000 |
| Categorias | ~72 |
| Preço Médio | R$ 120,77 |
| Período | 2016-09 a 2018-10 |

---

##  Links Úteis

- **Kaggle Dataset**: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
- **GitHub Repo**: https://github.com/HenriqueForin0905/TrabalhoBigData
- **Pandas Docs**: https://pandas.pydata.org/
- **Parquet**: https://parquet.apache.org/

---

##  Próximos Passos

1. Clone o repositório ✓
2. Instale dependências ✓
3. Teste com sample_data ✓
4. Baixe dados do Kaggle
5. Execute pipeline completo
6. Integre com BI tool
7. Explore EDA notebook
8. Customize KPIs conforme necessário

---

**Pronto para começar? Veja README.md!**
