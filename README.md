# Pipeline MLOps para Modelo em Produção

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![MLflow](https://img.shields.io/badge/MLflow-2.22.1-orange.svg)](https://mlflow.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Este projeto implementa um pipeline MLOps para detecção de fraude em transações financeiras, incluindo treinamento, experimentação, versionamento e deploy do modelo.

## Estrutura do Projeto

```
.
├── data/
│   ├── raw/           # Dados brutos
│   └── processed/     # Dados processados
├── src/
│   ├── data/         # Scripts de processamento de dados
│   ├── training/     # Scripts de treinamento
│   └── serve.py      # Script Python para servir o modelo com Flask
├── models/           # Modelos salvos (ignorados pelo git)
├── tests/            # Testes unitários
├── Dockerfile        # Configuração do container
└── requirements.txt  # Dependências do projeto
```

## Configuração do Ambiente

### Pré-requisitos
- Python 3.8+
- pip

### Instalação das Dependências
```bash
pip install -r requirements.txt
```

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
- Registrar métricas, parâmetros e artefatos no MLflow
- Salvar o melhor modelo localmente

## Análise de Experimentos (MLflow UI)

Após o treinamento, acesse a interface do MLflow para visualizar os experimentos:

```powershell
mlflow ui --port 51099 --backend-store-uri sqlite:///mlruns/mlflow.db --default-artifact-root mlruns
```
Abra no navegador: `http://127.0.0.1:51099`

Na UI do MLflow, você poderá:
- Comparar os runs e as métricas de cada configuração
- Visualizar os parâmetros usados em cada treinamento
- Analisar a matriz de confusão gerada para cada run

## Deploy Local do Modelo (API com Flask)

Para disponibilizar o modelo para inferência, usamos um servidor Flask que carrega o modelo salvo.

### 1. Iniciar o Servidor Flask
```powershell
python -m src.serve
```
O servidor estará disponível em `http://localhost:5001`.

### 2. Exemplo de Uso da API

Crie um arquivo `input.json` com os dados de entrada:

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

Envie uma requisição POST:
```powershell
Invoke-RestMethod -Uri http://localhost:5001/predict -Method Post -ContentType "application/json" -InFile input.json
```

A resposta será a predição do modelo (0 para não fraude, 1 para fraude).

## Monitoramento

O MLflow fornece:
- Rastreamento de experimentos
- Métricas de performance
- Versionamento de modelos
- Comparação entre diferentes execuções

## Próximos Passos

1. Implementar testes automatizados
2. Configurar CI/CD
3. Adicionar monitoramento de drift
4. Implementar retreinamento automático
5. Adicionar logging e alertas

## 🎯 Objetivo

Criar um pipeline que:
- Treina modelos de ML de forma reprodutível
- Versiona experimentos e modelos
- Disponibiliza o modelo via API REST
- Monitora performance do modelo

## 📫 Contato

Juliano Matheus - julianomatheusferreira@gmail.com - [GitHub](https://github.com/juliano1805)

Link do Projeto: [https://github.com/juliano1805/Pipeline-MLOPs-Themis](https://github.com/juliano1805/Pipeline-MLOPs-Themis) 