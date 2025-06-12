import mlflow
import mlflow.sklearn
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score
import os
import joblib
from src.config import (
    MLFLOW_TRACKING_URI, MLFLOW_EXPERIMENT,
    MLFLOW_ARTIFACT_ROOT, MODEL_CONFIGS,
    RANDOM_STATE, CV_SPLITS,
    PROCESSED_DIR, MODELS_DIR, MODEL_PATH
)

def treina_modelo():
    """Treina o modelo de detecção de fraude"""
    print("Iniciando treinamento...")
    
    # Configura MLflow
    print("Configurando MLflow...")
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    print(f"MLflow Tracking URI: {mlflow.get_tracking_uri()}")
    print(f"MLflow Artifact Root: {MLFLOW_ARTIFACT_ROOT}")
    
    # Cria ou obtém o experimento
    try:
        experiment = mlflow.get_experiment_by_name(MLFLOW_EXPERIMENT)
        if experiment is None:
            print(f"Criando novo experimento: {MLFLOW_EXPERIMENT}")
            experiment_id = mlflow.create_experiment(
                MLFLOW_EXPERIMENT,
                artifact_location=MLFLOW_ARTIFACT_ROOT
            )
        else:
            print(f"Usando experimento existente: {MLFLOW_EXPERIMENT}")
            experiment_id = experiment.experiment_id
        
        mlflow.set_experiment(experiment_id=experiment_id)
        print(f"MLflow Experiment ID: {experiment_id}")
    except Exception as e:
        print(f"Erro ao configurar experimento: {e}")
        return
    
    # Carrega dados
    print("Carregando dados...")
    try:
        print("Carregando X_train...")
        X_train = np.load(f"{PROCESSED_DIR}/X_train.npy")
        print(f"X_train carregado. Shape: {X_train.shape}")
        
        print("Carregando y_train...")
        y_train = np.load(f"{PROCESSED_DIR}/y_train.npy")
        print(f"y_train carregado. Shape: {y_train.shape}")
        
        print("Carregando X_test...")
        X_test = np.load(f"{PROCESSED_DIR}/X_test.npy")
        print(f"X_test carregado. Shape: {X_test.shape}")
        
        print("Carregando y_test...")
        y_test = np.load(f"{PROCESSED_DIR}/y_test.npy")
        print(f"y_test carregado. Shape: {y_test.shape}")
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return
    
    # Treina modelos
    print("\nIniciando treinamento dos modelos...")
    melhor_score = 0
    melhor_modelo = None
    
    for i, config in enumerate(MODEL_CONFIGS, 1):
        print(f"\n=== Configuração {i}/{len(MODEL_CONFIGS)} ===")
        print(f"Parâmetros: {config}")
        
        with mlflow.start_run(run_name=f"config_{i}"):
            print("Criando modelo...")
            modelo = RandomForestClassifier(
                random_state=RANDOM_STATE,
                **config
            )
            
            # Loga parâmetros do modelo
            print("Logando parâmetros do modelo...")
            mlflow.log_params({
                "model_type": "RandomForest",
                "random_state": RANDOM_STATE,
                **config
            })
            
            print("Realizando validação cruzada...")
            scores = cross_val_score(
                modelo, X_train, y_train,
                cv=CV_SPLITS, scoring='f1'
            )
            score_medio = scores.mean()
            print(f"Score médio CV: {score_medio:.4f}")
            
            # Loga métricas de validação cruzada
            mlflow.log_metrics({
                "cv_score_mean": score_medio,
                "cv_score_std": scores.std(),
                "cv_score_min": scores.min(),
                "cv_score_max": scores.max()
            })
            
            print("Treinando modelo final...")
            modelo.fit(X_train, y_train)
            
            print("Calculando métricas...")
            y_pred = modelo.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            
            # Gera e salva a matriz de confusão
            salva_matriz_confusao(y_test, y_pred, mlflow.active_run().info.run_id)
            
            print(f"Métricas:")
            print(f"- Accuracy: {accuracy:.4f}")
            print(f"- Precision: {precision:.4f}")
            print(f"- Recall: {recall:.4f}")
            print(f"- F1-Score: {f1:.4f}")
            
            # Loga métricas de teste
            print("Logando métricas de teste...")
            mlflow.log_metrics({
                "test_accuracy": accuracy,
                "test_precision": precision,
                "test_recall": recall,
                "test_f1": f1
            })
            
            # Loga tags para facilitar filtragem
            mlflow.set_tags({
                "model_type": "RandomForest",
                "dataset": "credit_card_fraud",
                "cv_folds": CV_SPLITS,
                "is_best_model": f1 > melhor_score
            })
            
            print(f"Run ID: {mlflow.active_run().info.run_id}")
            print(f"Experiment ID: {mlflow.active_run().info.experiment_id}")
            
            # Salva modelo
            print("Salvando modelo no MLflow...")
            mlflow.sklearn.log_model(
                modelo, 
                "modelo",
                registered_model_name="fraud_detection_model",
                input_example=X_test[:1],  # Exemplo de entrada para inferência de assinatura
                signature=mlflow.models.infer_signature(X_test, y_pred)  # Inferência de assinatura
            )
            
            # Atualiza melhor modelo
            if f1 > melhor_score:
                melhor_score = f1
                melhor_modelo = modelo
                print("Novo melhor modelo encontrado!")
    
    # Registra melhor modelo
    if melhor_modelo is not None:
        print("\nSalvando melhor modelo...")
        try:
            # Tenta registrar no MLflow
            mlflow.register_model(
                f"runs:/{mlflow.active_run().info.run_id}/modelo",
                "melhor_modelo_fraude"
            )
            print("Modelo registrado no MLflow!")
        except Exception as e:
            print(f"Não foi possível registrar no MLflow: {e}")
        
        # Salva localmente
        print("Salvando modelo localmente...")
        os.makedirs(MODELS_DIR, exist_ok=True)
        joblib.dump(melhor_modelo, MODEL_PATH)
        print(f"Modelo salvo localmente em: {MODEL_PATH}")
    else:
        print("Nenhum modelo foi treinado!")

def salva_matriz_confusao(y_true, y_pred, run_id):
    """Gera e salva a matriz de confusão como artifact"""
    # ETAPA DE VERIFICAÇÃO: Vamos verificar o conteúdo das variáveis
    print("--- Verificando y_test e y_pred ---")
    print(f"Shape de y_test: {y_true.shape}")
    print(f"Valores únicos em y_test: {np.unique(y_true)}")
    print(f"Shape de y_pred: {y_pred.shape}")
    print(f"Valores únicos em y_pred: {np.unique(y_pred)}")
    print("------------------------------------")

    # 1. Calcular a matriz de confusão
    # Adicionamos labels=[0, 1] para garantir que a matriz seja sempre 2x2
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])

    # 2. Criar a figura para o gráfico
    plt.figure(figsize=(8, 6))
    labels_heatmap = ['Não Fraude', 'Fraude']

    # 3. Gerar o gráfico de calor (heatmap) com Seaborn
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=labels_heatmap,
                yticklabels=labels_heatmap)

    plt.xlabel('Valor Predito')
    plt.ylabel('Valor Real')
    plt.title('Matriz de Confusão')

    # 4. Salvar o gráfico como um arquivo de imagem
    plt.savefig("matriz_de_confusao.png")

    # 5. Registrar a imagem como um artefato no MLflow
    mlflow.log_artifact("matriz_de_confusao.png", "plots")

    # Remove o arquivo temporário
    os.remove('matriz_de_confusao.png')

if __name__ == "__main__":
    treina_modelo() 