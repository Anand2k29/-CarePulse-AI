EMERGENCY_SYMPTOMS = [
    "chest_pain",
    "breathlessness",
    "unconsciousness",
    "severe_bleeding"
]

def check_emergency(symptoms):
    for symptom in symptoms:
        if symptom in EMERGENCY_SYMPTOMS:
            return True
    return False