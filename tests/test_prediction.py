import requests
import numpy as np
import json

def testa_predicao():
    """Testa a predição usando a API"""
    # URL da API
    url = "http://127.0.0.1:8000/prediz"
    
    # Dados de exemplo (uma transação normal)
    dados_normais = {
        "features": [0.0] * 29  # 29 features zeradas (transação normal)
    }
    
    # Dados de exemplo (uma transação suspeita)
    dados_suspeitos = {
        "features": [
            1.0,  # V1
            -1.0, # V2
            2.0,  # V3
            -2.0, # V4
            3.0,  # V5
            -3.0, # V6
            4.0,  # V7
            -4.0, # V8
            5.0,  # V9
            -5.0, # V10
            6.0,  # V11
            -6.0, # V12
            7.0,  # V13
            -7.0, # V14
            8.0,  # V15
            -8.0, # V16
            9.0,  # V17
            -9.0, # V18
            10.0, # V19
            -10.0,# V20
            11.0, # V21
            -11.0,# V22
            12.0, # V23
            -12.0,# V24
            13.0, # V25
            -13.0,# V26
            14.0, # V27
            -14.0,# V28
            15.0  # V29
        ]
    }
    
    # Testa transação normal
    print("\n=== Testando Transação Normal ===")
    try:
        response = requests.post(url, json=dados_normais)
        response.raise_for_status()
        resultado = response.json()
        print(f"Probabilidade de fraude: {resultado['prob_fraude']:.4f}")
        print(f"É fraude? {'Sim' if resultado['eh_fraude'] else 'Não'}")
    except Exception as e:
        print(f"Erro: {e}")
    
    # Testa transação suspeita
    print("\n=== Testando Transação Suspeita ===")
    try:
        response = requests.post(url, json=dados_suspeitos)
        response.raise_for_status()
        resultado = response.json()
        print(f"Probabilidade de fraude: {resultado['prob_fraude']:.4f}")
        print(f"É fraude? {'Sim' if resultado['eh_fraude'] else 'Não'}")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    testa_predicao() 