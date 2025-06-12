import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.model_selection import cross_val_score, StratifiedKFold
import os
import json

# Configurações que vamos testar
CONFIGS = [
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

def carrega_dados():
    """Carrega os dados processados"""
    print("Carregando dados...")
    X_train = np.load('data/processed/X_train.npy')
    X_test = np.load('data/processed/X_test.npy')
    y_train = np.load('data/processed/y_train.npy')
    y_test = np.load('data/processed/y_test.npy')
    print(f"Dados carregados. Tamanho do treino: {X_train.shape}")
    return X_train, X_test, y_train, y_test

def calcula_metricas(y_true, y_pred, y_pred_proba):
    """Calcula as métricas de avaliação"""
    return {
        "acuracia": accuracy_score(y_true, y_pred),
        "precisao": precision_score(y_true, y_pred),
        "recall": recall_score(y_true, y_pred),
        "f1": f1_score(y_true, y_pred),
        "roc_auc": roc_auc_score(y_true, y_pred_proba)
    }

def salva_importancia(modelo, X_train):
    """Salva a importância das features"""
    importancia = pd.DataFrame({
        'feature': [f'V{i}' for i in range(X_train.shape[1])],
        'importancia': modelo.feature_importances_
    }).sort_values('importancia', ascending=False)
    
    arquivo = 'data/processed/importancia_features.csv'
    importancia.to_csv(arquivo, index=False)
    mlflow.log_artifact(arquivo)

def treina_e_avalia(config, X_train, X_test, y_train, y_test, cv):
    """Treina e avalia um modelo com uma configuração específica"""
    with mlflow.start_run(nested=True):
        # Registra parâmetros
        mlflow.log_params(config)
        
        # Treina modelo
        print("Treinando...")
        modelo = RandomForestClassifier(**config, random_state=42)
        
        # Validação cruzada
        print("Validando...")
        scores_cv = cross_val_score(modelo, X_train, y_train, cv=cv, scoring='roc_auc')
        media_score = scores_cv.mean()
        std_score = scores_cv.std()
        
        mlflow.log_metric("media_score", media_score)
        mlflow.log_metric("std_score", std_score)
        
        # Treina com todos os dados
        print("Treinando modelo final...")
        modelo.fit(X_train, y_train)
        
        # Avalia no conjunto de teste
        print("Calculando métricas...")
        pred = modelo.predict(X_test)
        pred_proba = modelo.predict_proba(X_test)[:, 1]
        
        # Calcula métricas
        metricas = calcula_metricas(y_test, pred, pred_proba)
        for nome, valor in metricas.items():
            mlflow.log_metric(nome, valor)
        
        # Salva modelo e importância
        print("Salvando modelo...")
        mlflow.sklearn.log_model(modelo, "modelo_fraude")
        salva_importancia(modelo, X_train)
        
        # Mostra resultados
        print("\nResultados desta configuração:")
        print(f"ROC AUC (CV): {media_score:.4f} (+/- {std_score:.4f})")
        print(f"ROC AUC (Test): {metricas['roc_auc']:.4f}")
        print(f"Precisão: {metricas['precisao']:.4f}")
        print(f"Recall: {metricas['recall']:.4f}")
        print(f"F1-Score: {metricas['f1']:.4f}")
        
        return modelo, metricas["roc_auc"]

def treina_modelo():
    """Função principal de treinamento"""
    print("\n=== Iniciando Treinamento ===")
    
    # Configura MLflow
    print("Configurando MLflow...")
    mlflow.set_tracking_uri("http://127.0.0.1:51099")
    mlflow.set_experiment("Fraud Detection")
    
    # Carrega dados
    X_train, X_test, y_train, y_test = carrega_dados()
    
    # Prepara validação cruzada
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    # Inicializa variáveis para melhor modelo
    melhor_score = 0
    melhor_config = None
    melhor_modelo = None
    
    # Testa cada configuração
    print("\nTestando diferentes configurações...")
    for i, config in enumerate(CONFIGS, 1):
        print(f"\n=== Configuração {i}/{len(CONFIGS)} ===")
        print(f"Parâmetros: {config}")
        
        modelo, score = treina_e_avalia(config, X_train, X_test, y_train, y_test, cv)
        
        if score > melhor_score:
            melhor_score = score
            melhor_config = config
            melhor_modelo = modelo
            print("Novo melhor modelo encontrado!")
    
    # Salva melhor modelo
    print("\n=== Salvando Melhor Modelo ===")
    with mlflow.start_run(run_name="melhor_modelo"):
        mlflow.log_params(melhor_config)
        mlflow.sklearn.log_model(melhor_modelo, "melhor_modelo_fraude")
        
        # Salva configuração
        with open('data/processed/melhor_config.json', 'w') as f:
            json.dump(melhor_config, f)
        mlflow.log_artifact('data/processed/melhor_config.json')
        
        print("\nMelhor modelo encontrado:")
        print(f"Configuração: {melhor_config}")
        print(f"ROC AUC: {melhor_score:.4f}")
        print("\n=== Treinamento Concluído ===")

if __name__ == "__main__":
    treina_modelo() 