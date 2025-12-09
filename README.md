# E-Commerce Price Variation Pipeline

Projeto para análise de variações de preços em e-commerce usando o dataset Olist (Brazilian E-Commerce Public Dataset).

Estrutura mínima:

- `src/` - scripts do pipeline (`ingestao.py`, `processamento.py`, `gold.py`)
- `infra/` - infra opcional (ex.: `docker-compose.yaml` com MinIO)
- `Datasets/` - Data Lake em camadas: `Source`, `Raw`, `Bronze`, `Silver`, `Gold`
- `docs/` - documentação (Confluence template)
- `diagrams/` - diagramas (Mermaid)

Rápido guia de execução

1. Instale dependências:

```powershell
python -m pip install -r requirements.txt
```

2. Ingestão (executa `ingestao.py` já presente em `src`):

```powershell
python .\src\ingestao.py
```

3. Processamento para Silver:

```powershell
python .\src\processamento.py
```

4. Gerar Gold (KPIs):

```powershell
python .\src\gold.py
```

5. Aponte seu BI (Power BI / Metabase) para a pasta `Datasets/Gold`.

Obs: veja `infra/docker-compose.yaml` para uma opção com MinIO local.
