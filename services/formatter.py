import pandas as pd

class ResponseFormatter:
    def __init__(self):
        self.desc_df = pd.read_csv("data/symptom_Description.csv")
        self.prec_df = pd.read_csv("data/symptom_precaution.csv")
        
        # Clean disease name columns
        self.desc_df["Disease"] = self.desc_df["Disease"].str.strip().replace({
            "Dimorphic hemmorhoids(piles)": "Dimorphic hemorrhoids(piles)"
        })
        self.prec_df["Disease"] = self.prec_df["Disease"].str.strip().replace({
            "Dimorphic hemmorhoids(piles)": "Dimorphic hemorrhoids(piles)"
        })

    def format(self, disease, risk_level, severity_score,
               matched_symptoms, confidence, top3):

        # Clean disease name
        disease_clean = disease.strip().replace("Dimorphic hemmorhoids(piles)", "Dimorphic hemorrhoids(piles)")

        # Safe description retrieval
        description_row = self.desc_df[self.desc_df["Disease"] == disease_clean]
        if len(description_row) > 0:
            description = description_row["Description"].values[0]
        else:
            description = f"No description available for {disease_clean}."

        # Safe precautions retrieval
        precaution_row = self.prec_df[self.prec_df["Disease"] == disease_clean]
        if len(precaution_row) > 0:
            precautions = precaution_row.iloc[0, 1:].dropna().tolist()
        else:
            precautions = []

        # Make symptoms readable
        matched_readable = [
            s.replace("_", " ").capitalize()
            for s in matched_symptoms
        ]

        top3_formatted = [
            {
                "Disease": d.strip().replace("Dimorphic hemmorhoids(piles)", "Dimorphic hemorrhoids(piles)"),
                "Probability_percent": round(p * 100, 2)
            }
            for d, p in top3
        ]

        return {
            "Possible_Condition": disease_clean,
            "Matched_Symptoms": matched_readable,
            "Description": description,
            "Recommended_Precautions": precautions,
            "Risk_Level": risk_level,
            "Severity_Score": severity_score,
            "Confidence_percent": round(confidence, 2),
            "Top_3_Predictions": top3_formatted,
            "Disclaimer": "This is not a medical diagnosis. Please consult a qualified doctor."
        }