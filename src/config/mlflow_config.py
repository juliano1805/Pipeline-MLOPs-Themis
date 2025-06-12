import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configurações do MLflow
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
MLFLOW_EXPERIMENT_NAME = os.getenv("MLFLOW_EXPERIMENT_NAME", "modelo-producao")
MLFLOW_MODEL_NAME = os.getenv("MLFLOW_MODEL_NAME", "modelo-producao")

# Configurações do Modelo
MODEL_PARAMS = {
    "learning_rate": 0.001,
    "batch_size": 32,
    "epochs": 10,
    "validation_split": 0.2
}

# Configurações de Dados
DATA_CONFIG = {
    "raw_data_path": "data/raw",
    "processed_data_path": "data/processed",
    "train_test_split": 0.8
}

# Configurações de Deploy
DEPLOY_CONFIG = {
    "model_serving_name": "modelo-producao-serving",
    "namespace": "mlops",
    "replicas": 2
} 