import pandas as pd

class FollowUpEngine:
    def __init__(self):
        self.df = pd.read_csv("data/dataset.csv")
        self.df.fillna("", inplace=True)
        # Clean disease name
        self.df["Disease"] = self.df["Disease"].str.strip().replace({
            "Dimorphic hemmorhoids(piles)": "Dimorphic hemorrhoids(piles)"
        })
        # Clean symptom columns
        for col in self.df.columns[1:]:
            self.df[col] = self.df[col].astype(str).str.strip().str.replace(" ", "")

    def suggest_followup(self, predicted_disease, user_symptoms):
        # Clean input disease name to match clean dataframe keys
        disease_clean = predicted_disease.strip().replace("Dimorphic hemmorhoids(piles)", "Dimorphic hemorrhoids(piles)")
        disease_rows = self.df[self.df["Disease"] == disease_clean]

        all_symptoms = set()
        for _, row in disease_rows.iterrows():
            all_symptoms.update(row[1:])

        # Ensure user_symptoms are clean
        user_symptoms_clean = {s.strip().replace(" ", "") for s in user_symptoms}

        missing = list(all_symptoms - user_symptoms_clean)
        missing = [m for m in missing if m != ""]

        # Convert to readable format
        formatted = [m.replace("_", " ").capitalize() for m in missing[:3]]

        return formatted