import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

df = pd.read_csv("data/dataset.csv")
df.fillna("", inplace=True)

# Clean disease names
df["Disease"] = df["Disease"].str.strip().replace({
    "Dimorphic hemmorhoids(piles)": "Dimorphic hemorrhoids(piles)"
})

# Clean symptom columns
for col in df.columns[1:]:
    df[col] = df[col].astype(str).str.strip().str.replace(" ", "")

# Collect all unique symptoms
symptoms = set()
for col in df.columns[1:]:
    symptoms.update(df[col].unique())

symptoms.discard("")
symptoms = sorted(list(symptoms))

# Create binary matrix
X = []
for _, row in df.iterrows():
    row_symptoms = set(row[1:])
    X.append([1 if s in row_symptoms else 0 for s in symptoms])

X = np.array(X)
y = df["Disease"]

model = RandomForestClassifier(n_estimators=200)
model.fit(X, y)

joblib.dump((model, symptoms), "models/disease_model.pkl")

print("Model trained and saved.")