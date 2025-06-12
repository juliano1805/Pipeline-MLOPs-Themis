import os
import requests
from tqdm import tqdm
from src.config import RAW_DIR, DATASET_URL

def baixa_dados():
    """Baixa o dataset de fraude"""
    # Cria diretório
    os.makedirs(RAW_DIR, exist_ok=True)
    
    # Caminho do arquivo
    arquivo = f"{RAW_DIR}/creditcard.csv"
    
    # Verifica se já existe
    if os.path.exists(arquivo):
        print("Dataset já existe!")
        return
    
    print("Baixando dataset...")
    
    try:
        # Baixa o arquivo
        resposta = requests.get(DATASET_URL, stream=True)
        tamanho_total = int(resposta.headers.get('content-length', 0))
        
        with open(arquivo, 'wb') as f, tqdm(
            desc="Progresso",
            total=tamanho_total,
            unit='iB',
            unit_scale=True
        ) as barra:
            for dados in resposta.iter_content(chunk_size=1024):
                tamanho = f.write(dados)
                barra.update(tamanho)
                
        print("Download concluído!")
        
    except Exception as e:
        print(f"Erro ao baixar: {e}")
        if os.path.exists(arquivo):
            os.remove(arquivo)

if __name__ == "__main__":
    baixa_dados() 