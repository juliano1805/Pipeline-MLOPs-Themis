# Imagem base
FROM python:3.8-slim

# Diretório de trabalho
WORKDIR /app

# Copia arquivos
COPY requirements.txt .
COPY src/ src/

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe porta
EXPOSE 8000

# Inicia API
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"] 