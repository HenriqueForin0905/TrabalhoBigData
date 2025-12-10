# Infraestrutura - Guia Completo

Este diretório contém configurações de infraestrutura para o pipeline de dados.

## 📋 Visão Geral

| Componente | Tipo | Status | Uso |
|-----------|------|--------|-----|
| **Docker Compose** | Orquestração | ✅ Incluído | MinIO local (S3-compatible) |
| **MinIO** | Object Storage | ✅ Incluído | Armazenamento distribuído (opcional) |
| **Terraform** | IaC | ⏳ Futuro | Deploy em cloud (AWS, Azure, GCP) |
| **Kubernetes** | Container Orchestration | ⏳ Futuro | Escalabilidade enterprise |

---

## 🐳 Docker Compose + MinIO

### O que é MinIO?

MinIO é um servidor compatível com Amazon S3 que pode ser executado localmente. Ideal para:
- Desenvolvimento e testes
- Armazenamento de dados em camadas (Raw, Bronze, Silver, Gold)
- Integração com ferramentas de big data (Spark, Dask)
- Backup e replicação

### Arquitetura

```
┌─────────────────────────────────────────┐
│     Docker Container (MinIO)            │
├─────────────────────────────────────────┤
│ Porta 9000 (API): Upload/Download dados │
│ Porta 9001 (UI): Console web            │
├─────────────────────────────────────────┤
│  Storage: ./minio/data (volume docker)  │
└─────────────────────────────────────────┘
```

### Inicializar MinIO

#### Pré-requisitos

- Docker Desktop instalado
- Docker Compose (incluído no Docker Desktop)

#### Comando de Inicialização

```powershell
# Inicie o MinIO
cd .\infra
docker-compose up -d

# Verifique status
docker ps | grep minio
```

#### Acesso

- **Console Web**: http://localhost:9001
- **API Endpoint**: http://localhost:9000
- **Username**: minioadmin
- **Password**: minioadmin

#### Criar Buckets

```powershell
# Via CLI (AWS S3 CLI compatível)
aws --endpoint-url http://localhost:9000 s3 mb s3://raw-data
aws --endpoint-url http://localhost:9000 s3 mb s3://bronze-data
aws --endpoint-url http://localhost:9000 s3 mb s3://silver-data
aws --endpoint-url http://localhost:9000 s3 mb s3://gold-data
```

Ou via Console Web:
1. Acesse http://localhost:9001
2. Faça login (minioadmin/minioadmin)
3. Clique em **Create Bucket** (+)
4. Nomeie: `raw-data`, `bronze-data`, `silver-data`, `gold-data`

#### Upload de Dados

```powershell
# Upload de CSVs para S3
aws --endpoint-url http://localhost:9000 s3 cp .\Datasets\Source\ s3://raw-data/ --recursive

# Verifique
aws --endpoint-url http://localhost:9000 s3 ls s3://raw-data/
```

#### Parar MinIO

```powershell
# Parar container
docker-compose down

# Parar e limpar volumes
docker-compose down -v
```

### Configurar Pipeline para Usar MinIO

Modifique `src/ingestao.py`:

```python
from minio import Minio
from minio.error import S3Error

client = Minio(
    "localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

# Upload de dados
def upload_to_minio(file_path, bucket, object_name):
    try:
        client.fput_object(bucket, object_name, file_path)
        print(f"✅ Uploaded {object_name} to {bucket}")
    except S3Error as e:
        print(f"❌ Error: {e}")

# Download de dados
def download_from_minio(bucket, object_name, file_path):
    try:
        client.fget_object(bucket, object_name, file_path)
        print(f"✅ Downloaded {object_name} from {bucket}")
    except S3Error as e:
        print(f"❌ Error: {e}")
```

### Monitoramento

```powershell
# Ver logs do MinIO
docker logs minio

# Ver uso de disco
docker exec minio du -sh /data

# Stats em tempo real
docker stats minio
```

---

## ☁️ Terraform (Futuro)

Planejado para deploy em cloud:

### AWS (Planned)

```hcl
# main.tf
resource "aws_s3_bucket" "data_lake" {
  bucket = "ecommerce-data-lake"
  acl    = "private"
}

resource "aws_lambda_function" "pipeline" {
  filename = "lambda.zip"
  role     = aws_iam_role.lambda_role.arn
  handler  = "index.handler"
}

resource "aws_glue_crawler" "bronze_crawler" {
  database_name = "bronze_db"
  role          = aws_iam_role.glue_role.arn
}
```

### Azure (Planned)

```hcl
# main.tf
resource "azurerm_storage_account" "data_lake" {
  name                     = "ecommercedatalake"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = "Brazil South"
  account_tier             = "Standard"
  account_replication_type = "GRS"
}
```

### Google Cloud (Planned)

```hcl
# main.tf
resource "google_storage_bucket" "data_lake" {
  name          = "ecommerce-data-lake"
  location      = "SOUTHAMERICA-EAST1"
  force_destroy = false
}
```

---

## 🎯 Kubernetes (Futuro)

Para escalabilidade enterprise:

```yaml
# pipeline-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ecommerce-pipeline
spec:
  replicas: 3
  selector:
    matchLabels:
      app: pipeline
  template:
    metadata:
      labels:
        app: pipeline
    spec:
      containers:
      - name: pipeline
        image: ecommerce-pipeline:latest
        resources:
          requests:
            memory: "2Gi"
            cpu: "500m"
```

---

## 🔐 Segurança

### MinIO Local

```powershell
# Mudar credenciais padrão (antes de iniciar)
# Edite docker-compose.yaml:
# MINIO_ROOT_USER=seu_usuario
# MINIO_ROOT_PASSWORD=sua_senha_forte

# Gere certificados SSL (produção)
minio server --certs-dir /path/to/certs /data
```

### Credenciais em Cloud

```bash
# AWS
export AWS_ACCESS_KEY_ID="seu_access_key"
export AWS_SECRET_ACCESS_KEY="sua_secret_key"

# GCP
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"

# Azure
az login
```

### Variáveis de Ambiente

Nunca comite credenciais! Use `.env`:

```bash
# .env (não commitar)
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=secure_password_123
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

```python
# load_env.py
from dotenv import load_dotenv
import os

load_dotenv()
minio_user = os.getenv('MINIO_ROOT_USER')
minio_pass = os.getenv('MINIO_ROOT_PASSWORD')
```

---

## 📊 Monitoramento e Alertas

### Prometheus + Grafana (Futuro)

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'minio'
    static_configs:
      - targets: ['localhost:9000']
```

### CloudWatch (AWS)

```python
import boto3
import logging

cloudwatch = boto3.client('logs')

def log_pipeline(status, message):
    cloudwatch.put_log_events(
        logGroupName='/aws/lambda/ecommerce-pipeline',
        logStreamName='main',
        logEvents=[{
            'timestamp': int(time.time() * 1000),
            'message': f"[{status}] {message}"
        }]
    )
```

---

## 🚀 Deploy em Produção

### Checklist

- [ ] Configurar credenciais em `.env`
- [ ] Testar pipeline localmente
- [ ] Criar backups dos dados
- [ ] Configurar monitoring
- [ ] Implementar alertas
- [ ] Documentar runbooks
- [ ] Treinar equipe

### GitHub Actions CI/CD (Futuro)

```yaml
# .github/workflows/deploy.yml
name: Deploy Pipeline

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: python -m pytest tests/
      - name: Deploy
        run: |
          docker build -t pipeline:latest .
          docker push myregistry/pipeline:latest
```

---

## 📈 Escalabilidade

### Evolução da Infraestrutura

```
Fase 1: Local (Atuall)
  ├─ File System (Local)
  └─ Python Scripts (Serial)

Fase 2: Híbrida
  ├─ MinIO (Local + Cloud)
  └─ PySpark (Paralelo)

Fase 3: Cloud Native
  ├─ S3 (AWS / Azure / GCP)
  ├─ Airflow (Orchestração)
  ├─ Glue / Dataflow (ETL)
  └─ Databricks / BigQuery (Warehouse)

Fase 4: Enterprise
  ├─ Multi-Cloud
  ├─ Kubernetes
  ├─ Real-time Streaming (Kafka)
  └─ Data Lakehouse (Delta Lake / Iceberg)
```

---

## 🔗 Links Úteis

- **MinIO Docs**: https://min.io/docs/minio/container/
- **Docker Compose**: https://docs.docker.com/compose/
- **AWS S3**: https://aws.amazon.com/s3/
- **Terraform**: https://www.terraform.io/
- **Kubernetes**: https://kubernetes.io/

---

## 💡 Dicas

1. **Desenvolvimento Local**: Use MinIO + Docker Compose
2. **Testes**: Use dados de amostra (sample_data/)
3. **Produção**: Migre para cloud (AWS/Azure/GCP)
4. **CI/CD**: Configure GitHub Actions para deploy automático
5. **Monitoring**: Use CloudWatch, Prometheus ou DataDog

---

**Última Atualização:** Dezembro 2025
