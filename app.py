from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

feature_names = [
    'temperature', 'humidity', 'precipitation', 'wind_speed',
    'elevation', 'slope', 'soil_ph', 'soil_organic_carbon',
    'land_cover_class', 'month', 'day_of_year'
]

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'service': 'bioshield-predict-ml',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No input data'}), 400
        
        # Заглушка за тест: изчислява риск на база температура и влажност
        risk = min(100, max(0, 
            (data.get('temperature', 20) - 15) * 5 + 
            (data.get('humidity', 60) - 50) * 0.5
        ))
        
        return jsonify({
            'risk_percent': float(risk),
            'risk_class': 1 if risk > 50 else 0,
            'note': 'Тестов режим (без обучен модел)'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/features', methods=['GET'])
def get_features():
    return jsonify({
        'features': feature_names,
        'count': len(feature_names)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
