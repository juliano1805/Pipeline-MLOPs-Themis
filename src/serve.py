import joblib
from flask import Flask, request, jsonify, Response
import numpy as np
import logging
from prometheus_client import generate_latest, Counter

app = Flask(__name__)

# Configurar o logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s')

# Métricas Prometheus
requests_total = Counter('http_requests_total', 'Total de requisições HTTP', ['method', 'endpoint', 'status'])
errors_total = Counter('http_errors_total', 'Total de erros HTTP', ['method', 'endpoint', 'status'])

# Carregar o modelo
try:
    model = joblib.load('models/melhor_modelo.joblib')
    logging.info("Modelo 'melhor_modelo.joblib' carregado com sucesso.")
except FileNotFoundError:
    logging.error("Erro: O arquivo do modelo 'models/melhor_modelo.joblib' não foi encontrado.")
    model = None # Definir modelo como None para evitar NameError
except Exception as e:
    logging.error(f"Erro ao carregar o modelo: {e}")
    model = None

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        logging.error("Tentativa de predição, mas o modelo não foi carregado.")
        requests_total.labels('POST', '/predict', '503').inc()
        errors_total.labels('POST', '/predict', '503').inc()
        return jsonify({'error': 'O modelo não está disponível. Por favor, verifique os logs do servidor.'}), 503

    try:
        data = request.get_json()
        if data is None:
            logging.warning("Requisição recebida sem payload JSON.")
            requests_total.labels('POST', '/predict', '400').inc()
            errors_total.labels('POST', '/predict', '400').inc()
            return jsonify({'error': 'Payload JSON ausente ou malformado.'}), 400
        
        # Logar a requisição recebida
        logging.info(f"Requisição recebida: {data}")

        if 'features' not in data:
            logging.warning("Campo 'features' ausente na requisição.")
            requests_total.labels('POST', '/predict', '400').inc()
            errors_total.labels('POST', '/predict', '400').inc()
            return jsonify({'error': 'O campo \'features\' é obrigatório no payload JSON.'}), 400

        features = np.array(data['features'])
        
        # Validação do formato das features
        if features.ndim != 1 or features.shape[0] != 29:
            logging.warning(f"Formato de features inválido: {features.shape}. Esperado: (29,).")
            requests_total.labels('POST', '/predict', '400').inc()
            errors_total.labels('POST', '/predict', '400').inc()
            return jsonify({'error': 'Formato de features inválido. Esperado um array de 29 features.'}), 400

        prediction_proba = model.predict_proba(features.reshape(1, -1))[0][1] # Probabilidade da classe positiva (fraude)
        prediction_class = bool(model.predict(features.reshape(1, -1))[0])

        response = {
            'prob_fraude': float(prediction_proba),
            'eh_fraude': prediction_class
        }
        logging.info(f"Predição bem-sucedida: {response}")
        requests_total.labels('POST', '/predict', '200').inc()
        return jsonify(response)

    except ValueError as ve:
        logging.error(f"Erro de validação de dados na predição: {ve}")
        requests_total.labels('POST', '/predict', '400').inc()
        errors_total.labels('POST', '/predict', '400').inc()
        return jsonify({'error': f'Erro de validação de dados: {str(ve)}'}), 400
    except TypeError as te:
        logging.error(f"Erro de tipo de dado na predição: {te}")
        requests_total.labels('POST', '/predict', '400').inc()
        errors_total.labels('POST', '/predict', '400').inc()
        return jsonify({'error': f'Erro de tipo de dado: {str(te)}'}), 400
    except Exception as e:
        logging.exception("Erro inesperado durante a predição:") # loga o traceback
        requests_total.labels('POST', '/predict', '500').inc()
        errors_total.labels('POST', '/predict', '500').inc()
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001) 