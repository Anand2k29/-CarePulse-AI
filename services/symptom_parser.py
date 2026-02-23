import re

class SymptomParser:
    def __init__(self, known_symptoms):
        self.known_symptoms = known_symptoms

    def normalize_text(self, text):
        text = text.lower()
        text = re.sub(r"[^\w\s]", " ", text)
        return text

    def parse(self, text):
        text = self.normalize_text(text)
        detected = []

        for symptom in self.known_symptoms:
            readable = symptom.replace("_", " ")
            if readable in text:
                detected.append(symptom)

        return list(set(detected))