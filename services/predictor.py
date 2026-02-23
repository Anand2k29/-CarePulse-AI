import pandas as pd

class DiseasePredictor:
    def __init__(self):
        self.df = pd.read_csv("data/dataset.csv")
        self.df.fillna("", inplace=True)

    def predict(self, user_symptoms):
        user_symptoms = set(user_symptoms)

        best_match = None
        max_match_count = 0

        for _, row in self.df.iterrows():
            disease = row["Disease"]
            symptoms = set(row[1:])  # All symptom columns
            symptoms.discard("")

            match_count = len(user_symptoms.intersection(symptoms))

            if match_count > max_match_count:
                max_match_count = match_count
                best_match = disease

        return best_match, max_match_count