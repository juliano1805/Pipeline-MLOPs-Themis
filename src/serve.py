import joblib
from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)

# Carregar o modelo
model = joblib.load('models/melhor_modelo.joblib')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        features = np.array(data['dataframe_split']['data'])
        prediction = model.predict(features)
        return jsonify({'predictions': prediction.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001) 