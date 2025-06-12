# Pipeline MLOps para Detecção de Fraudes com MLflow, Flask e GitHub Actions

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![MLflow](https://img.shields.io/badge/MLflow-2.22.1-orange.svg)](https://mlflow.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![CI/CD Status](https://github.com/juliano1805/Pipeline-MLOPs-Themis/actions/workflows/main.yml/badge.svg)](https://github.com/juliano1805/Pipeline-MLOPs-Themis/actions/workflows/main.yml)

> 🧠 Projeto completo de MLOps para detecção de fraudes, com MLflow, Flask, Prometheus, GitHub Actions e testes automatizados.

---

## 🚀 Sobre o Projeto

Este projeto simula um **pipeline completo de Machine Learning pronto para produção**, com foco em detecção de fraudes em transações financeiras. Foi idealizado como uma vitrine técnica de MLOps e engenharia de modelos, aplicando práticas reais de deploy, monitoramento e versionamento.

### 🔍 Destaques

* **MLflow** para rastreamento, experimentação e registro de modelos.
* **Flask API** para servir o modelo com endpoint de predição e métricas.
* **Prometheus** para expor métricas de requisições da API.
* **GitHub Actions** para CI/CD automatizado.
* **Logging estruturado e testes com Pytest** para robustez e observabilidade.

💡 Ideal para empresas que buscam profissionais júnior com **base sólida em produção de modelos**, além de habilidades em engenharia e automação.

---

## 🧱 Estrutura do Projeto

```
.
├── .github/workflows/        # CI/CD com GitHub Actions
├── data/                     # Dados brutos e processados
├── src/
│   ├── data/                 # Scripts de tratamento
│   ├── training/             # Treinamento e validação
│   └── serve.py              # API Flask para inferência
├── models/                   # Modelos salvos (git-ignored)
├── tests/                    # Testes com pytest
├── Dockerfile                # Containerização opcional
└── requirements.txt          # Dependências
```

---

## ⚙️ Setup do Ambiente

### Pré-requisitos

* Python 3.9+
* pip instalado

### Instalar dependências

```bash
pip install -r requirements.txt
```

---

## 📊 Treinamento e Versionamento de Modelos

### 1. Preparar os dados

```bash
python src/data/download_data.py
```

### 2. Treinar e registrar modelo no MLflow

```bash
python src/train.py
```

* Cross-validation com grid de hiperparâmetros
* Registro automático de parâmetros, métricas e artefatos
* Versionamento no Model Registry do MLflow

### Interface MLflow

```bash
mlflow ui --port 51099 --backend-store-uri sqlite:///mlruns/mlflow.db
```

➡️ Acesse: [http://127.0.0.1:51099](http://127.0.0.1:51099)

---

## 🌐 Deploy do Modelo via API Flask

```bash
python -m src.serve
```

Endpoint local: `http://localhost:5001/predict`

### Exemplo de chamada via JSON

```json
{
  "features": [29 valores com features normalizadas...]
}
```

### Requisição (PowerShell ou Terminal)

```bash
Invoke-RestMethod -Uri http://localhost:5001/predict -Method Post -ContentType "application/json" -InFile input.json
```

---

## 📈 Monitoramento com Prometheus

A API expõe o endpoint `/metrics` para ferramentas como o Prometheus coletarem métricas:

* `http_requests_total`: Total de requisições por status
* `http_errors_total`: Total de erros por status HTTP

---

## ✅ Testes Automatizados

```bash
pytest tests/
```

Cobertura dos testes:

* API de predição
* Tratamento de erros
* Comportamentos esperados do modelo

---

## 🔁 CI/CD com GitHub Actions

Cada `push` ou `pull_request` aciona o workflow:

* Checkout do código
* Instalação do ambiente
* Execução dos testes

📦 Status: veja o badge no topo

---

## 🎯 Objetivos Técnicos

Este pipeline foi criado para demonstrar:

* 📌 Reprodutibilidade de experimentos com MLflow
* 📦 Deploy leve com Flask
* 🧪 Testes automatizados com pytest
* 🚦 Observabilidade e monitoramento via Prometheus
* 🔄 Automação de entrega com CI/CD no GitHub

---

## 📫 Contato

Juliano Matheus
📧 [julianomatheusferreira@gmail.com](mailto:julianomatheusferreira@gmail.com)
💼 [LinkedIn](https://www.linkedin.com/in/julianomatheusferreira)
👨‍💻 [GitHub](https://github.com/juliano1805)

Repositório: [https://github.com/juliano1805/Pipeline-MLOPs-Themis](https://github.com/juliano1805/Pipeline-MLOPs-Themis)

## 📊 Resultados

### Métricas do Melhor Modelo
* **Accuracy**: 0.9995
* **Precision**: 0.9059
* **Recall**: 0.7857
* **F1-Score**: 0.8415

### Validação Cruzada
* Score médio CV: 0.8299
* Configuração otimizada:
  * n_estimators: 200
  * max_depth: 15
  * min_samples_split: 3
  * min_samples_leaf: 1
  * class_weight: balanced

---

## 🛠️ Tecnologias

### Linguagens e Frameworks
* Python 3.9+
* Flask
* Scikit-learn
* MLflow 2.22.1

### DevOps e MLOps
* GitHub Actions
* Prometheus
* Docker (opcional)

### Testes e Qualidade
* Pytest
* Logging estruturado
* CI/CD automatizado

---

## 🚀 Próximos Passos

* **Containerização**
  * Implementação completa com Docker
  * Configuração de Docker Compose
  * Documentação de deployment

* **Monitoramento**
  * Adição de mais métricas de performance
  * Dashboard com Grafana
  * Alertas automáticos

* **Testes**
  * Aumento da cobertura de testes
  * Testes de integração
  * Testes de carga

* **CI/CD**
  * Pipeline de deployment automático
  * Ambientes de staging
  * Rollback automático

---

## 🤝 Como Contribuir

1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Padrões de Código
* Seguir PEP 8
* Documentar funções e classes
* Manter testes atualizados
* Atualizar documentação
