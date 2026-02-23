import joblib
import numpy as np

class MLPredictor:
    def __init__(self):
        self.model, self.symptom_list = joblib.load("models/disease_model.pkl")

    def predict(self, symptoms):
        input_vector = [1 if s in symptoms else 0 for s in self.symptom_list]
        input_vector = np.array(input_vector).reshape(1, -1)

        prediction = self.model.predict(input_vector)[0]
        probabilities = self.model.predict_proba(input_vector)[0]

        classes = self.model.classes_
        prob_dict = dict(zip(classes, probabilities))

        top3 = sorted(prob_dict.items(), key=lambda x: x[1], reverse=True)[:3]

        # Cap unrealistic confidence
        confidence = min(max(probabilities) * 100, 95)

        return prediction, confidence, top3