# Estrutura Completa do Repositório

##  Árvore de Diretórios

```
TrabalhoBigData/
│
├── docs/                                          [DOCUMENTAÇÃO]
│   ├── DOCUMENTACAO_GERAL.md                        #  Guia técnico completo (3.500+ linhas)
│   │   ├── Descrição do problema
│   │   ├── Objetivos do sistema
│   │   ├── Escopo da solução
│   │   ├── Arquitetura completa
│   │   ├── Ferramentas e tecnologias
│   │   ├── Decisões técnicas (trade-offs)
│   │   ├── Guia de execução
│   │   ├── Guia de dependências
│   │   ├── Descrição dos dados
│   │   ├── Pontos de falha e limitações
│   │   └── Troubleshooting
│   ├── confluence_export.md                         #  Formato Confluence (pronto para importar)
│   └── confluence_template.md                       #  Template para Confluence
│
├──  src/                                           [CÓDIGO-FONTE]
│   ├── README.md                                    #  Guia de scripts (explicação detalhada)
│   ├── ingestao.py                                  # 1 Raw → Bronze (normalização)
│   │   └── Normaliza nomes de colunas (snake_case)
│   ├── processamento.py                             # 2 Bronze → Silver (transformação)
│   │   └── Padroniza tipos, trata nulos, salva Parquet
│   ├── gold.py                                      # 3 Silver → Gold (KPIs)
│   │   ├── avg_price_by_category.csv
│   │   └── price_variation_by_month.csv
│   ├── processamento_fix.py                         # Versão otimizada (chunked reading)
│   └── gold_fix.py                                  # Versão otimizada (memory efficient)
│
├──  notebooks/                                    [ANÁLISE EXPLORATÓRIA]
│   └── 01_eda_olist.ipynb                          # 🔬 Jupyter Notebook - EDA
│       ├── Importação de bibliotecas
│       ├── Carregamento de dados
│       ├── Bronze Layer (limpeza)
│       ├── Silver Layer (transformação)
│       ├── Gold Layer (KPIs)
│       ├── Análise exploratória
│       └── Visualizações e insights
│
├──  infra/                                         [INFRAESTRUTURA]
│   ├── README.md                                    #  Guia de infraestrutura
│   │   ├── Docker Compose + MinIO
│   │   ├── Terraform (AWS, Azure, GCP)
│   │   ├── Kubernetes (futuro)
│   │   ├── Segurança e credenciais
│   │   ├── Monitoramento e alertas
│   │   └── Deploy em produção
│   └── docker-compose.yaml                         #  MinIO local (S3-compatible)
│       └── Portas: 9000 (API), 9001 (Console)
│
├──  datasets/                                      [DADOS E TESTES]
│   ├── README.md                                    #  Guia de dados
│   │   ├── Estrutura dos dados
│   │   ├── Dicionário de dados
│   │   ├── Estatísticas
│   │   └── Como usar
│   └── sample_data/                                 #  Dados de amostra (teste rápido)
│       ├── olist_orders_sample.csv                 # ~10 pedidos
│       ├── olist_order_items_sample.csv            # ~15 itens
│       ├── olist_products_sample.csv               # ~15 produtos
│       ├── olist_customers_sample.csv              # ~10 clientes
│       └── olist_sellers_sample.csv                # ~10 vendedores
│
├──  Datasets/                                      [DATA LAKE - CRIADO AUTOMATICAMENTE]
│   ├── Source/                                      # Dados originais (Kaggle)
│   ├── Raw/                                         # Cópia literal dos CSVs
│   ├── Bronze/                                      # Colunas normalizadas (CSV)
│   ├── Silver/                                      # Dados transformados (Parquet)
│   └── Gold/                                        # KPIs prontos para BI (CSV)
│
├──  diagrams/                                      [DIAGRAMAS]
│   └── architecture.mmd                            # Arquitetura Mermaid
│
├──  requirements.txt                              [DEPENDÊNCIAS PYTHON]
│   ├── pandas>=1.3
│   ├── pyarrow>=8.0
│   ├── fastparquet>=0.8
│   └── pyspark>=3.2  # opcional
│
└──  README.md                                     [GUIA PRINCIPAL]
    ├── Visão geral do projeto
    ├── Estrutura do repositório
    ├── Início rápido
    ├── Pipeline architecture
    ├── KPIs gerados
    ├── Integração com BI
    ├── Dados e estatísticas
    ├── Documentação
    ├── Comandos úteis
    ├── Configuração avançada
    ├── Troubleshooting
    ├── Próximos passos
    └── Referências
```

---

##  Resumo de Documentação

### Por Tipo

| Arquivo | Tipo | Público | Tamanho | Propósito |
|---------|------|---------|---------|-----------|
| **README.md** | Markdown | ✅ | ~2KB | Guia rápido e visão geral |
| **DOCUMENTACAO_GERAL.md** | Markdown | ✅ | ~100KB | Documentação técnica completa |
| **confluence_export.md** | Confluence Markup | ✅ | ~80KB | Pronto para importar no Confluence |
| **notebooks/01_eda_olist.ipynb** | Jupyter | ✅ | ~5KB | Análise exploratória interativa |
| **src/README.md** | Markdown | ✅ | ~30KB | Explicação de cada script |
| **infra/README.md** | Markdown | ✅ | ~25KB | Guia de infraestrutura |
| **datasets/README.md** | Markdown | ✅ | ~20KB | Dicionário e estatísticas de dados |

### Por Público-Alvo

```
 Diferentes Personas

├─  Gestor/Product Owner
│  └─ Leia: README.md + DOCUMENTACAO_GERAL.md (Visão Geral, Objetivos, Escopo)
│
├─  Desenvolvedor
│  └─ Leia: src/README.md + notebooks/01_eda_olist.ipynb
│
├─  DevOps/Infraestrutura
│  └─ Leia: infra/README.md + docker-compose.yaml
│
├─  Data Analyst
│  └─ Leia: datasets/README.md + notebooks/01_eda_olist.ipynb
│
└─  Iniciante
   └─ Leia: README.md → Guia de Execução → notebooks → src/README.md
```

---

##  Fluxo de Leitura Recomendado

### Para Iniciantes

1. ✅ **README.md** (5 min) - Entender o que é o projeto
2. ✅ **datasets/README.md** (10 min) - Conhecer os dados
3. ✅ **Executar Teste Rápido** (1 min) - `python .\src\ingestao.py`
4. ✅ **notebooks/01_eda_olist.ipynb** (15 min) - Ver análises e gráficos
5. ✅ **src/README.md** (20 min) - Entender cada script
6. ✅ **DOCUMENTACAO_GERAL.md** (30 min) - Detalhes técnicos

**Tempo Total: ~1.5 hora**

### Para Engenheiros de Dados

1. ✅ **README.md** (2 min) - Overview
2. ✅ **src/README.md** (15 min) - Scripts detalhados
3. ✅ **DOCUMENTACAO_GERAL.md** - Arquitetura + Decisões Técnicas
4. ✅ **infra/README.md** (10 min) - Infraestrutura
5. ✅ **Executar pipeline** (10 min) - Teste prático

**Tempo Total: ~1 hora**

### Para DevOps/Cloud

1. ✅ **infra/README.md** (10 min) - Começar aqui
2. ✅ **docker-compose.yaml** (5 min) - Entender MinIO
3. ✅ **README.md - Integração com BI** (5 min) - Casos de uso
4. ✅ **DOCUMENTACAO_GERAL.md - Decisões Técnicas** (20 min)

**Tempo Total: ~40 min**

---

##  Estatísticas do Repositório

### Documentação

| Métrica | Valor |
|---------|-------|
| Total de documentos Markdown | 7 |
| Linhas de documentação | ~4.000+ |
| Exemplos de código | 50+ |
| Diagramas | 5+ |
| Tabelas de referência | 30+ |

### Código

| Arquivo | Linhas | Função |
|---------|--------|--------|
| ingestao.py | ~80 | Normalização |
| processamento.py | ~50 | Transformação |
| gold.py | ~70 | Agregação |
| processamento_fix.py | ~100 | Otimização |
| gold_fix.py | ~120 | Otimização |
| **Total** | **~420** | **Pipeline completo** |

### Dados de Amostra

| Arquivo | Registros | Tamanho |
|---------|-----------|---------|
| olist_orders_sample.csv | 10 | ~1 KB |
| olist_order_items_sample.csv | 15 | ~1 KB |
| olist_products_sample.csv | 15 | ~2 KB |
| olist_customers_sample.csv | 10 | ~1 KB |
| olist_sellers_sample.csv | 10 | ~1 KB |
| **Total** | **60** | **~6 KB** |

---

##  Relacionamentos entre Documentos

```
README.md (Hub Central)
├─→ Guia de Execução → datasets/README.md (dados)
├─→ Arquitetura → DOCUMENTACAO_GERAL.md (técnica)
├─→ Scripts → src/README.md (código)
├─→ Infraestrutura → infra/README.md (ops)
├─→ Análise → notebooks/01_eda_olist.ipynb (EDA)
└─→ BI Integration → DOCUMENTACAO_GERAL.md (BI tools)

confluence_export.md
└─→ Cópia de DOCUMENTACAO_GERAL.md em formato Confluence
```

---

## ✅ Checklist de Leitura

- [ ] Li README.md
- [ ] Entendi o pipeline (Raw → Bronze → Silver → Gold)
- [ ] Executei teste rápido com sample_data
- [ ] Abri notebook de EDA
- [ ] Li explicação de cada script (src/README.md)
- [ ] Explorei infraestrutura (docker-compose)
- [ ] Consultei DOCUMENTACAO_GERAL.md para dúvidas
- [ ] Integrei com BI tool (Power BI / Metabase)
- [ ] Executei pipeline com dados completos do Kaggle
- [ ] Estou pronto para extensões/customizações!

---

##  Próximas Leituras Recomendadas

- [ ] Medallion Architecture (Delta Lake)
- [ ] Apache Airflow (Orchestração)
- [ ] PySpark (Processamento Distribuído)
- [ ] AWS Glue / Azure Synapse (Cloud)
- [ ] Data Quality & Monitoring

---

##  Última Atualização

**Data:** Dezembro 2025  
**Versão:** 1.0  
**Status:** ✅ Completa e documentada

---


