import kfp
from kfp import dsl
from kfp.components import func_to_container_op
from typing import NamedTuple

# Componente para preparação de dados
@func_to_container_op
def prepare_data() -> NamedTuple('Outputs', [('processed_data_path', str)]):
    from src.data.preprocessing import preprocess_data
    import os
    
    processed_data_path = preprocess_data()
    return (processed_data_path,)

# Componente para treinamento do modelo
@func_to_container_op
def train_model(processed_data_path: str) -> NamedTuple('Outputs', [('model_path', str)]):
    from src.training.train import train_model
    import os
    
    model_path = train_model(processed_data_path)
    return (model_path,)

# Componente para avaliação do modelo
@func_to_container_op
def evaluate_model(model_path: str, processed_data_path: str) -> NamedTuple('Outputs', [('metrics', dict)]):
    from src.training.evaluate import evaluate_model
    import json
    
    metrics = evaluate_model(model_path, processed_data_path)
    return (json.dumps(metrics),)

# Componente para deploy do modelo
@func_to_container_op
def deploy_model(model_path: str, metrics: str):
    from src.serving.deploy import deploy_model
    import json
    
    metrics_dict = json.loads(metrics)
    if metrics_dict['accuracy'] > 0.8:  # Threshold para deploy
        deploy_model(model_path)
    else:
        raise Exception("Modelo não atingiu o threshold mínimo de acurácia")

# Definição do pipeline
@dsl.pipeline(
    name='MLOps Pipeline',
    description='Pipeline completo de MLOps para treinamento e deploy de modelo'
)
def mlops_pipeline():
    # Etapas do pipeline
    prepare_data_task = prepare_data()
    train_model_task = train_model(prepare_data_task.outputs['processed_data_path'])
    evaluate_model_task = evaluate_model(
        train_model_task.outputs['model_path'],
        prepare_data_task.outputs['processed_data_path']
    )
    deploy_model_task = deploy_model(
        train_model_task.outputs['model_path'],
        evaluate_model_task.outputs['metrics']
    )

if __name__ == '__main__':
    # Compila o pipeline
    kfp.compiler.Compiler().compile(mlops_pipeline, 'mlops_pipeline.yaml') 