import re

class SymptomParser:
    def __init__(self, known_symptoms):
        self.known_symptoms = [s.strip().replace(" ", "") for s in known_symptoms]

    def normalize_text(self, text):
        text = text.lower()
        text = re.sub(r"[^\w\s]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def parse(self, text):
        text = self.normalize_text(text)
        detected = []

        for symptom in self.known_symptoms:
            readable = symptom.replace("_", " ")
            aliases = [readable]
            
            # Special variations/aliases for known typos/phrases in the dataset
            if symptom == "foul_smell_ofurine":
                aliases.append("foul smell of urine")
            elif symptom == "spotting_urination":
                aliases.append("spotting urination")
            elif symptom == "dischromic_patches":
                aliases.append("dischromic patches")
                aliases.append("discolored patches")
                aliases.append("patches on skin")

            for alias in aliases:
                if alias in text:
                    detected.append(symptom)
                    break

        return list(set(detected))