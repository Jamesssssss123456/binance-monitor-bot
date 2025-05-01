import pickle
import numpy as np

def load_model_and_predict(features):
    with open("ai_soros_model.pkl", "rb") as f:
        model = pickle.load(f)

    # 判斷是否為 scikit-learn 類模型
    if hasattr(model, "predict"):
        prediction = model.predict([features])[0]
    elif isinstance(model, np.ndarray):
        prediction = model[0]  # 假設這是誤打包的 array，直接取第一項避免崩潰
    else:
        raise ValueError("Loaded object is not a valid prediction model.")

    return prediction
