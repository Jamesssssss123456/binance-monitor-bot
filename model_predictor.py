
import pickle

def load_model_and_predict(features):
    with open("ai_soros_model.pkl", "rb") as f:
        model = pickle.load(f)
    prediction = model.predict([features])[0]
    return "long" if prediction == 1 else "short"
