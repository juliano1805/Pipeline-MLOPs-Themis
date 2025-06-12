import mlflow
import os
from src.config import MODEL_PATH, MODELS_DIR

def verifica_modelo():
    """Verifica o status do modelo"""
    print("=== Verificando Status do Modelo ===")
    
    # Verifica MLflow
    try:
        mlflow.set_tracking_uri("http://127.0.0.1:51099")
        experiment = mlflow.get_experiment_by_name("Fraud Detection")
        if experiment:
            print("\n✅ MLflow está rodando!")
            runs = mlflow.search_runs(experiment_ids=[experiment.experiment_id])
            if not runs.empty:
                print(f"Último run: {runs.iloc[0]['run_id']}")
                print(f"Métricas do último run:")
                print(f"- F1-Score: {runs.iloc[0]['metrics.f1']:.4f}")
                print(f"- Accuracy: {runs.iloc[0]['metrics.accuracy']:.4f}")
        else:
            print("\n❌ Nenhum experimento encontrado no MLflow")
    except Exception as e:
        print(f"\n❌ Erro ao acessar MLflow: {e}")
    
    # Verifica modelo local
    print("\n=== Verificando Modelo Local ===")
    if os.path.exists(MODEL_PATH):
        print(f"✅ Modelo encontrado em: {MODEL_PATH}")
        print(f"Tamanho: {os.path.getsize(MODEL_PATH) / 1024 / 1024:.2f} MB")
    else:
        print(f"❌ Modelo não encontrado em: {MODEL_PATH}")

if __name__ == "__main__":
    verifica_modelo() 