import pandas as pd

class SeverityEngine:
    def __init__(self):
        self.severity_df = pd.read_csv("data/Symptom-severity.csv")
        self.severity_df["Symptom"] = self.severity_df["Symptom"].str.strip().str.replace(" ", "")
        self.severity_dict = dict(
            zip(self.severity_df["Symptom"],
                self.severity_df["weight"])
        )

    def calculate_score(self, symptoms):
        return sum(self.severity_dict.get(s, 0) for s in symptoms)

    def get_risk_level(self, score):
        if score >= 15:
            return "High"
        elif score >= 7:
            return "Medium"
        else:
            return "Low"