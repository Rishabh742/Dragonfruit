from flask import request, jsonify
from app import app
from app.utils import load_keras_model
import numpy as np

model = load_keras_model('app/model/model.h5')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    features = np.array(data['features']).reshape(1, -1)  # Reshape for single sample prediction
    prediction = model.predict(features)
    return jsonify({'prediction': prediction.tolist()})
