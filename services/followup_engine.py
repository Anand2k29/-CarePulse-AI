import pandas as pd

class FollowUpEngine:
    def __init__(self):
        self.df = pd.read_csv("data/dataset.csv")
        self.df.fillna("", inplace=True)

    def suggest_followup(self, predicted_disease, user_symptoms):
        disease_rows = self.df[self.df["Disease"] == predicted_disease]

        all_symptoms = set()
        for _, row in disease_rows.iterrows():
            all_symptoms.update(row[1:])

        missing = list(all_symptoms - set(user_symptoms))
        missing = [m for m in missing if m != ""]

        # Convert to readable format
        formatted = [m.replace("_", " ").capitalize() for m in missing[:3]]

        return formatted