import mlflow
import joblib
import os
from src.config import MODEL_PATH, MODELS_DIR

def salva_modelo():
    """Salva o modelo atual do MLflow localmente"""
    try:
        # Configura MLflow
        mlflow.set_tracking_uri("http://127.0.0.1:51099")
        
        # Busca o último run
        experiment = mlflow.get_experiment_by_name("Fraud Detection")
        if not experiment:
            raise Exception("Experimento não encontrado")
            
        runs = mlflow.search_runs(experiment_ids=[experiment.experiment_id])
        if runs.empty:
            raise Exception("Nenhum run encontrado")
            
        ultimo_run = runs.iloc[0]
        run_id = ultimo_run['run_id']
        
        # Carrega o modelo do último run
        modelo = mlflow.sklearn.load_model(f"runs:/{run_id}/modelo")
        print(f"✅ Modelo carregado do run: {run_id}")
        
        # Cria diretório se não existir
        os.makedirs(MODELS_DIR, exist_ok=True)
        
        # Salva localmente
        joblib.dump(modelo, MODEL_PATH)
        print(f"✅ Modelo salvo com sucesso em: {MODEL_PATH}")
        
        # Mostra métricas
        print("\nMétricas do modelo:")
        print(f"- F1-Score: {ultimo_run['metrics.f1']:.4f}")
        print(f"- Accuracy: {ultimo_run['metrics.accuracy']:.4f}")
        
    except Exception as e:
        print(f"❌ Erro ao salvar modelo: {e}")

if __name__ == "__main__":
    salva_modelo() 