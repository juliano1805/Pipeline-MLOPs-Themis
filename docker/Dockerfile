# Imagem base
FROM python:3.8-slim

# Define variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho
WORKDIR /app

# Copia os requisitos primeiro para aproveitar o cache do Docker
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copia o código fonte
COPY src/ src/
COPY pipeline/ pipeline/

# Expõe a porta para o servidor do modelo
EXPOSE 8080

# Comando para iniciar o servidor
CMD ["python", "src/serving/serve.py"] 