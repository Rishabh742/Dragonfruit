from tensorflow.keras.models import load_model

def load_keras_model(path):
    model = load_model(path)
    return model
