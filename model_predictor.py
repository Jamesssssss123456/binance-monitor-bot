import pickle

def load_model_and_predict(features):
    with open("ai_soros_model.pkl", "rb") as f:
        model = pickle.load(f)
    return model.predict([features])[0]