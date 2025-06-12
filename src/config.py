import os

# Configurações do MLflow
MLFLOW_TRACKING_URI = f"sqlite:///{os.path.abspath('mlruns/mlflow.db')}"
MLFLOW_EXPERIMENT = "Fraud Detection"
MLFLOW_ARTIFACT_ROOT = f"file:///{os.path.normpath(os.path.abspath('mlruns')).replace('\\', '/')}"

# Garante que o diretório mlruns existe com as permissões corretas
os.makedirs(os.path.abspath("mlruns"), exist_ok=True)

# Configurações do modelo
MODEL_CONFIGS = [
    {
        "n_estimators": 100,
        "max_depth": 10,
        "min_samples_split": 5,
        "min_samples_leaf": 2,
        "class_weight": "balanced"
    },
    {
        "n_estimators": 200,
        "max_depth": 15,
        "min_samples_split": 3,
        "min_samples_leaf": 1,
        "class_weight": "balanced"
    },
    {
        "n_estimators": 150,
        "max_depth": 12,
        "min_samples_split": 4,
        "min_samples_leaf": 2,
        "class_weight": "balanced_subsample"
    }
]

# Configurações de treinamento
RANDOM_STATE = 42
TEST_SIZE = 0.2
CV_SPLITS = 5

# Caminhos dos arquivos
DATA_DIR = "data"
RAW_DIR = f"{DATA_DIR}/raw"
PROCESSED_DIR = f"{DATA_DIR}/processed"
MODELS_DIR = "models"
MODEL_PATH = f"{MODELS_DIR}/melhor_modelo.joblib"

# URLs
DATASET_URL = "https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud/download"

# Configurações da API
API_HOST = "0.0.0.0"
API_PORT = 8000
API_TITLE = "API de Detecção de Fraude"
API_DESCRIPTION = "API para prever fraudes em transações"
API_VERSION = "1.0.0" 