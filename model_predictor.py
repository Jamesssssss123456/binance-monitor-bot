
import joblib

def load_model_and_predict(features):
    model = joblib.load("ai_soros_model.pkl")
    return model.predict([features])[0]
