import pandas as pd

class ResponseFormatter:
    def __init__(self):
        self.desc_df = pd.read_csv("data/symptom_Description.csv")
        self.prec_df = pd.read_csv("data/symptom_precaution.csv")

    def format(self, disease, risk_level, severity_score,
               matched_symptoms, confidence, top3):

        description = self.desc_df[
            self.desc_df["Disease"] == disease
        ]["Description"].values[0]

        precautions = self.prec_df[
            self.prec_df["Disease"] == disease
        ].iloc[0, 1:].dropna().tolist()

        # Make symptoms readable
        matched_readable = [
            s.replace("_", " ").capitalize()
            for s in matched_symptoms
        ]

        top3_formatted = [
            {
                "Disease": d,
                "Probability_percent": round(p * 100, 2)
            }
            for d, p in top3
        ]

        return {
            "Possible_Condition": disease,
            "Matched_Symptoms": matched_readable,
            "Description": description,
            "Recommended_Precautions": precautions,
            "Risk_Level": risk_level,
            "Severity_Score": severity_score,
            "Confidence_percent": round(confidence, 2),
            "Top_3_Predictions": top3_formatted,
            "Disclaimer": "This is not a medical diagnosis. Please consult a qualified doctor."
        }