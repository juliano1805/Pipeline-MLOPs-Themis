import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os
import joblib
from src.config import (
    PROCESSED_DIR, RAW_DIR, RANDOM_STATE, 
    TEST_SIZE
)

def processa_dados():
    """Processa os dados brutos para treinamento"""
    print("Processando dados...")
    
    # Cria diretórios
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    
    # Carrega dados
    print("Carregando dados brutos...")
    dados = pd.read_csv(f"{RAW_DIR}/creditcard.csv")
    
    # Separa features e target
    X = dados.drop('Class', axis=1)
    y = dados['Class']
    
    # Divide em treino e teste
    print("Dividindo em treino e teste...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    
    # Normaliza features
    print("Normalizando features...")
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    # Salva dados processados
    print("Salvando dados processados...")
    np.save(f"{PROCESSED_DIR}/X_train.npy", X_train)
    np.save(f"{PROCESSED_DIR}/X_test.npy", X_test)
    np.save(f"{PROCESSED_DIR}/y_train.npy", y_train)
    np.save(f"{PROCESSED_DIR}/y_test.npy", y_test)
    
    # Salva scaler
    joblib.dump(scaler, f"{PROCESSED_DIR}/scaler.joblib")
    
    print("Dados processados com sucesso!")
    print(f"Shape dos dados de treino: {X_train.shape}")
    print(f"Shape dos dados de teste: {X_test.shape}")

if __name__ == "__main__":
    processa_dados() 