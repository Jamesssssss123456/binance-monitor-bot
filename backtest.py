import pandas as pd
from model_predictor import load_model_and_predict
from indicator_utils import extract_features

df = pd.read_csv("voxel_training_dataset.csv")
correct = 0
total = 0

for _, row in df.iterrows():
    features = [row['f1'], row['f2'], row['f3'], row['f4'], row['f5']]
    label = row['label']
    prediction = load_model_and_predict(features)
    if prediction == label:
        correct += 1
    total += 1

print(f"Accuracy: {correct / total:.2%}")