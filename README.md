# Pipeline MLOps para Modelo em Produção

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![MLflow](https://img.shields.io/badge/MLflow-2.22.1-orange.svg)](https://mlflow.org/)
[![Kubeflow](https://img.shields.io/badge/Kubeflow-2.0.0-blue.svg)](https://www.kubeflow.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Este projeto implementa um pipeline MLOps completo para detecção de fraude em transações financeiras, incluindo treinamento, experimentação, versionamento e deploy do modelo.

## Estrutura do Projeto

```
.
├── data/
│   ├── raw/           # Dados brutos
│   └── processed/     # Dados processados
├── src/
│   ├── data/         # Scripts de processamento de dados
│   ├── training/     # Scripts de treinamento
│   ├── api/          # API para servir o modelo
│   └── serve.py      # Script Python para servir o modelo com Flask
├── models/           # Modelos salvos (ignorados pelo git)
├── tests/            # Testes unitários (incluindo test_prediction.py)
├── Dockerfile        # Configuração do container
└── requirements.txt  # Dependências do projeto
```

## Configuração do Ambiente

### Pré-requisitos
- Python 3.8+
- Docker Desktop
- Minikube
- kubectl

### Instalação das Dependências
```bash
pip install -r requirements.txt
```

## Configuração do MLflow no Kubernetes

### 1. Iniciar o Minikube
```powershell
# Abra o PowerShell como administrador
cd "C:\Pipeline MLOps para Modelo em Producao"
minikube start --driver=docker --memory=3000 --cpus=4
```

### 2. Aplicar a Configuração do MLflow
```powershell
kubectl apply -f mlflow-deployment.yaml
```

### 3. Verificar o Status do Pod
```powershell
kubectl get pods
# Aguarde até ver o status "Running"
```

### 4. Acessar a Interface do MLflow
```powershell
minikube service mlflow --url
```
Copie o endereço retornado e cole no seu navegador.

**Importante:** Mantenha o terminal aberto enquanto estiver usando o MLflow.

## Treinamento do Modelo

### 1. Preparar os Dados
```powershell
python src/data/download_data.py
```

### 2. Treinar o Modelo
```powershell
python src/train.py
```

O script irá:
- Realizar validação cruzada
- Testar diferentes configurações de hiperparâmetros
- Registrar métricas, parâmetros e artefatos (incluindo matriz de confusão) no MLflow
- Salvar o melhor modelo localmente e no MLflow Model Registry

## Análise de Experimentos e Decisão do Modelo (MLflow UI)

Após o treinamento, acesse a interface do MLflow para visualizar os experimentos e as métricas de cada configuração:

```powershell
mlflow ui --port 51099 --backend-store-uri sqlite:///mlruns/mlflow.db --default-artifact-root mlruns
```
Abra no navegador: `http://127.0.0.1:51099`

Na UI do MLflow, você poderá:
- Comparar os runs e as métricas de cada configuração.
- Visualizar os parâmetros usados em cada treinamento.
- Analisar a matriz de confusão gerada e salva como artefato para cada run.
- **Explicação da Decisão:** Demonstre como a "Configuração 2" (ou a configuração com o melhor F1-Score/balanceamento entre precisão e recall, dependendo do seu foco) foi selecionada como o "melhor modelo" com base nas métricas de teste (especialmente o F1-Score, que é crucial para problemas de classificação desbalanceada como fraude). Mostre os detalhes do run escolhido, seus parâmetros, métricas e artefatos.

## Deploy Local do Modelo (API com Flask)

Para disponibilizar o modelo para inferência, usaremos um servidor Flask simples que carrega o modelo salvo.

### 1. Iniciar o Servidor Flask
Certifique-se de que o servidor Flask está rodando. Se o servidor MLflow UI estiver em execução em outro terminal, abra um **novo terminal** e execute:

```powershell
python -m src.serve
```
O servidor estará disponível em `http://localhost:5001`.

### 2. Exemplo de Uso da API

Crie um arquivo `input.json` no diretório raiz do seu projeto com os dados de entrada para o modelo (o formato esperado é `dataframe_split` conforme utilizado pelo MLflow Serving):

```json
{
  "dataframe_split": {
    "columns": [
      "V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9", "V10",
      "V11", "V12", "V13", "V14", "V15", "V16", "V17", "V18", "V19", "V20",
      "V21", "V22", "V23", "V24", "V25", "V26", "V27", "V28", "Amount"
    ],
    "data": [
      [
        -0.42861348, 0.95758079, 0.40794421, 0.4437166, -0.06109918,
        -0.12932631, 0.49071077, 0.15858054, -0.27967918, -0.45789647,
        -0.24430485, 0.15082159, -0.06316279, -0.23118944, -0.19946896,
        -0.09459392, -0.10804705, -0.03848293, -0.01548058, 0.05286548,
        -0.10091398, -0.20786938, -0.27503713, -0.20239077, 0.28786937,
        0.12467389, 0.06312458, 0.06312458, 10.00
      ]
    ]
  }
}
```

Então, use o PowerShell para enviar uma requisição POST:

```powershell
Invoke-RestMethod -Uri http://localhost:5001/predict -Method Post -ContentType "application/json" -InFile input.json
```

A resposta da API será a predição do modelo (0 para não fraude, 1 para fraude).

## Monitoramento

O MLflow fornece:
- Rastreamento de experimentos
- Métricas de performance
- Versionamento de modelos
- Comparação entre diferentes execuções

Acesse a interface web do MLflow para visualizar:
- Gráficos de métricas
- Importância das features
- Parâmetros dos modelos
- Artefatos salvos

## Próximos Passos

1. Implementar testes automatizados
2. Configurar CI/CD
3. Adicionar monitoramento de drift
4. Implementar retreinamento automático
5. Adicionar logging e alertas

## 🎯 Objetivo

Criar um pipeline automatizado que:
- Treina modelos de ML de forma reprodutível
- Versiona experimentos e modelos
- Faz deploy em ambiente Kubernetes
- Monitora performance em produção

## 🏗️ Arquitetura

O pipeline é composto por:

1. **Preparação de Dados**
   - ETL com PySpark
   - Pré-processamento
   - Validação de dados

2. **Treinamento**
   - Experimentos com MLflow
   - Modelos TensorFlow/PyTorch
   - Versionamento de artefatos

3. **Pipeline MLOps**
   - Kubeflow Pipelines
   - CI/CD com ArgoCD
   - GitOps para versionamento

4. **Deploy e Monitoramento**
   - Kubernetes
   - Kubeflow Serving
   - Monitoramento com Prometheus/Grafana

## 📁 Estrutura do Projeto

```
.
├── data/                   # Dados brutos e processados (ignorados pelo git)
├── notebooks/             # Jupyter notebooks para experimentação
├── src/                   # Código fonte
│   ├── data/             # Scripts de ETL
│   ├── models/           # Definição dos modelos
│   ├── training/         # Scripts de treinamento
│   └── serve.py          # Código para servir o modelo com Flask
├── pipeline/             # Definições do Kubeflow Pipeline
├── k8s/                  # Manifests Kubernetes
├── tests/                # Testes automatizados
└── docker/               # Dockerfiles
```

## 🚀 Como Usar

### Pré-requisitos

- Python 3.12
- Docker
- Kubernetes cluster
- Kubeflow
- MLflow

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/mlops-pipeline.git
cd mlops-pipeline
```

2. Crie e ative o ambiente virtual:
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate # Linux/Mac
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp env.example .env
# Edite o arquivo .env com suas configurações
```

### Executando o Pipeline

1. Inicie o MLflow:
```bash
mlflow server
```

2. Execute o pipeline:
```bash
python src/pipeline/run_pipeline.py
```

## 📊 Monitoramento

- MLflow UI: http://localhost:5000
- Grafana Dashboard: http://localhost:3000
- Prometheus: http://localhost:9090

## 🧪 Testes

Execute os testes automatizados:
```bash
pytest tests/
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie sua branch de feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📫 Contato

Seu Nome - [@seu_twitter](https://twitter.com/seu_twitter) - email@exemplo.com

Link do Projeto: [https://github.com/seu-usuario/mlops-pipeline](https://github.com/seu-usuario/mlops-pipeline)

## Configuração do Ambiente

### Pré-requisitos
- Python 3.8+
- Docker Desktop
- Minikube
- kubectl

### Instalação das Dependências
```bash
pip install -r requirements.txt
```

## Configuração do MLflow no Kubernetes

### 1. Iniciar o Minikube
```powershell
# Abra o PowerShell como administrador
cd "C:\Pipeline MLOps para Modelo em Producao"
minikube start --driver=docker --memory=3000 --cpus=4
```

### 2. Aplicar a Configuração do MLflow
```powershell
kubectl apply -f mlflow-deployment.yaml
```

### 3. Verificar o Status do Pod
```powershell
kubectl get pods
# Aguarde até ver o status "Running"
```

### 4. Acessar a Interface do MLflow
```powershell
minikube service mlflow --url
```
Copie o endereço retornado (exemplo: http://127.0.0.1:52323) e cole no seu navegador.

**Importante:** Mantenha o terminal aberto enquanto estiver usando o MLflow, pois o serviço depende dele para continuar rodando. 