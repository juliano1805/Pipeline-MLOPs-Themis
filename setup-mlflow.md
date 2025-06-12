# Configuração do MLflow

## 1. Instalar o MLflow

```powershell
# Instalar o MLflow e suas dependências
pip install mlflow psycopg2-binary
```

## 2. Configurar o banco de dados PostgreSQL para o MLflow

### Instalar o PostgreSQL (usando Chocolatey)
```powershell
choco install postgresql
```

### Criar o banco de dados
```powershell
# Conectar ao PostgreSQL
psql -U postgres

# No prompt do PostgreSQL:
CREATE DATABASE mlflow;
CREATE USER mlflow WITH ENCRYPTED PASSWORD 'mlflow';
GRANT ALL PRIVILEGES ON DATABASE mlflow TO mlflow;
\q
```

## 3. Iniciar o servidor MLflow

```powershell
# Criar diretório para artefatos
mkdir mlflow-artifacts

# Iniciar o servidor MLflow
mlflow server ^
    --backend-store-uri postgresql://mlflow:mlflow@localhost/mlflow ^
    --default-artifact-root ./mlflow-artifacts ^
    --host 0.0.0.0 ^
    --port 5000
```

## 4. Configurar as variáveis de ambiente

Edite o arquivo `.env` com as seguintes configurações:
```env
MLFLOW_TRACKING_URI=http://localhost:5000
MLFLOW_EXPERIMENT_NAME=modelo-producao
MLFLOW_MODEL_NAME=modelo-producao
```

## 5. Testar a configuração

```powershell
# Criar um script Python de teste
python -c "
import mlflow
mlflow.set_tracking_uri('http://localhost:5000')
mlflow.set_experiment('teste-mlflow')
with mlflow.start_run():
    mlflow.log_param('param1', 5)
    mlflow.log_metric('metric1', 0.8)
"

# Verificar no navegador:
# http://localhost:5000
```

## 6. Configurar o MLflow no Kubernetes

```powershell
# Criar namespace para o MLflow
kubectl create namespace mlflow

# Aplicar o manifesto do MLflow
kubectl apply -f k8s/mlflow-deployment.yaml
```

## 7. Verificar a instalação no Kubernetes

```powershell
# Verificar os pods do MLflow
kubectl get pods -n mlflow

# Expor o serviço do MLflow
kubectl port-forward svc/mlflow -n mlflow 5000:5000
``` 