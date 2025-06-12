# Script para instalar todas as dependências

# Criar e ativar ambiente virtual Python
python -m venv venv
.\venv\Scripts\Activate

# Atualizar pip
python -m pip install --upgrade pip

# Instalar dependências do projeto
pip install -r requirements.txt

# Instalar dependências adicionais para desenvolvimento
pip install black flake8 pytest pytest-cov

Write-Host "Dependências instaladas com sucesso!"
Write-Host "Para ativar o ambiente virtual, execute: .\venv\Scripts\Activate" 