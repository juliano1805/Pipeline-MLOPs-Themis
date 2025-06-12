from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import mlflow
import joblib
from typing import List
from src.config import (
    MLFLOW_TRACKING_URI, API_TITLE, 
    API_DESCRIPTION, API_VERSION,
    API_HOST, API_PORT, MODEL_PATH
)

# Configuração da API
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION
)

# Modelo de dados
class Transacao(BaseModel):
    """Dados de entrada para predição"""
    features: List[float]

class Predicao(BaseModel):
    """Resultado da predição"""
    prob_fraude: float
    eh_fraude: bool
    limite: float = 0.5

# Carrega o modelo
def carrega_modelo():
    """Carrega o modelo treinado"""
    try:
        # Tenta carregar do MLflow
        return mlflow.sklearn.load_model("models:/melhor_modelo_fraude/Production")
    except:
        try:
            # Tenta carregar do MLflow (versão latest)
            return mlflow.sklearn.load_model("models:/melhor_modelo_fraude/latest")
        except:
            # Carrega do arquivo local
            return joblib.load(MODEL_PATH)

modelo = carrega_modelo()

# Rotas
@app.get("/")
def inicio():
    """Página inicial"""
    return {
        "mensagem": "API de Detecção de Fraude - Use /docs para ver a documentação"
    }

@app.post("/prediz", response_model=Predicao)
def prediz(transacao: Transacao):
    """Faz a predição de fraude"""
    try:
        # Prepara dados
        features = np.array(transacao.features).reshape(1, -1)
        
        # Faz predição
        prob_fraude = modelo.predict_proba(features)[0, 1]
        eh_fraude = prob_fraude > 0.5
        
        return Predicao(
            prob_fraude=float(prob_fraude),
            eh_fraude=bool(eh_fraude)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao fazer predição: {str(e)}"
        )

@app.get("/info-modelo")
def info_modelo():
    """Informações sobre o modelo"""
    try:
        return {
            "tipo": type(modelo).__name__,
            "num_features": modelo.n_features_in_,
            "nomes_features": [f"V{i}" for i in range(modelo.n_features_in_)],
            "parametros": modelo.get_params()
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar informações: {str(e)}"
        )

# Inicia servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT) 