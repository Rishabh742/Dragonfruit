from flask import Flask, request, jsonify
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image
import io

app = Flask(__name__)

# Load your Keras model here
quality_model = load_model('app/model/quality_model.h5')
maturity_model = load_model('app/model/maturity_model.h5')

@app.route('/quality-grading', methods=['POST'])
def quality_grading():
    file = request.files['file']
    img = Image.open(io.BytesIO(file.read()))
    img = img.resize((224, 224))  # Resize image to match model input if needed
    img_array = np.array(img) / 255.0  # Normalize if required by the model
    img_array = np.expand_dims(img_array, axis=0)
    prediction = quality_model.predict(img_array)
    result = np.argmax(prediction, axis=1)[0]  # Example of processing the prediction
    return jsonify({"result": str(result)})

@app.route('/maturity-detection', methods=['POST'])
def maturity_detection():
    file = request.files['file']
    img = Image.open(io.BytesIO(file.read()))
    img = img.resize((224, 224))  # Resize image to match model input if needed
    img_array = np.array(img) / 255.0  # Normalize if required by the model
    img_array = np.expand_dims(img_array, axis=0)
    prediction = maturity_model.predict(img_array)
    result = np.argmax(prediction, axis=1)[0]  # Example of processing the prediction
    return jsonify({"result": str(result)})

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    features = np.array(data['features']).reshape(1, -1)  # Adjust shape as needed for your model
    prediction = quality_model.predict(features)  # Example: using quality_model for prediction
    result = prediction[0].tolist()  # Convert prediction to list
    return jsonify({'prediction': result})

if __name__ == '__main__':
    app.run(debug=True)
