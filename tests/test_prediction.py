import requests
import numpy as np
import json

def test_prediction_api_normal_transaction():
    """
    Testa a predição para uma transação normal, verificando se a API retorna
    "eh_fraude": False e uma probabilidade de fraude baixa.
    """
    # URL da API
    url = "http://127.0.0.1:5001/predict"
    
    # Dados de exemplo para uma transação normal (29 features zeradas)
    dados_normais = {
        "features": [0.0] * 29  
    }
    
    print("\n=== Testando Transação Normal === (test_prediction_api_normal_transaction)")
    try:
        response = requests.post(url, json=dados_normais)
        response.raise_for_status()  # Levanta um HTTPError para 4xx/5xx responses
        resultado = response.json()
        print(f"Probabilidade de fraude: {resultado['prob_fraude']:.4f}")
        print(f"É fraude? {'Sim' if resultado['eh_fraude'] else 'Não'}")

        # Asserções para uma transação normal
        assert "prob_fraude" in resultado
        assert "eh_fraude" in resultado
        assert not resultado["eh_fraude"]  # Espera que não seja fraude
        assert resultado["prob_fraude"] < 0.5 # Espera uma probabilidade baixa

    except requests.exceptions.ConnectionError:
        print("Erro de Conexão: Certifique-se de que o servidor Flask esteja em execução na porta 5001.")
        raise
    except Exception as e:
        print(f"Erro inesperado durante o teste de transação normal: {e}")
        raise

def test_prediction_api_suspicious_transaction():
    """
    Testa a predição para uma transação suspeita, verificando se a API retorna
    "eh_fraude": True e uma probabilidade de fraude alta.
    """
    # URL da API
    url = "http://127.0.0.1:5001/predict"

    # Dados de exemplo para uma transação suspeita (valores altos para algumas features)
    dados_suspeitos = {
        "features": [
            1.0, -1.0, 2.0, -2.0, 3.0, -3.0, 4.0, -4.0, 5.0, -5.0,
            6.0, -6.0, 7.0, -7.0, 8.0, -8.0, 9.0, -9.0, 10.0, -10.0,
            11.0, -11.0, 12.0, -12.0, 13.0, -13.0, 14.0, -14.0, 15.0
        ]
    }
    
    print("\n=== Testando Transação Suspeita === (test_prediction_api_suspicious_transaction)")
    try:
        response = requests.post(url, json=dados_suspeitos)
        response.raise_for_status()
        resultado = response.json()
        print(f"Probabilidade de fraude: {resultado['prob_fraude']:.4f}")
        print(f"É fraude? {'Sim' if resultado['eh_fraude'] else 'Não'}")

        # Asserções para uma transação suspeita
        assert "prob_fraude" in resultado
        assert "eh_fraude" in resultado
        assert resultado["eh_fraude"]  # Espera que seja fraude
        assert resultado["prob_fraude"] >= 0.5 # Espera uma probabilidade alta

    except requests.exceptions.ConnectionError:
        print("Erro de Conexão: Certifique-se de que o servidor Flask esteja em execução na porta 5001.")
        raise
    except Exception as e:
        print(f"Erro inesperado durante o teste de transação suspeita: {e}")
        raise

# A função 'testa_predicao' e o bloco '__main__' são removidos
# para que o pytest possa descobrir e executar as funções de teste. 