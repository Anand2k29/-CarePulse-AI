# CarePulse AI 🏥
### Intelligent Medical Symptom Analyzer & Triage Assistant

CarePulse AI is a local-first, Machine Learning-powered clinical support engine. It translates natural, free-text symptom descriptions from patients into structured, data-driven disease predictions, calculates clinical severity indexes, suggests follow-up inquiries, and screens for life-threatening medical emergencies.



## 📌 What It Is About
Traditional medical databases require users to select checkboxes from exhaustive symptom lists. CarePulse AI innovates on this by letting users type their conditions in natural language (e.g., *"I have had a sharp chest pain, high fever, and I'm feeling very short of breath"*). 

The application utilizes:
1. **Natural Language Parsing**: Maps sentences to clean, standardized symptom identifiers.
2. **Random Forest Classifier**: Feeds a binary vector into an ML model trained on thousands of diagnostic combinations to classify the most probable disease.
3. **Clinical Severity Scoring**: Aggregates weights corresponding to the matched symptoms.
4. **Emergency Triage Check**: Inspects vectors for critical symptoms (such as chest pain or breathlessness) to immediately flag emergency conditions.

---

## 🚀 Key Features

* **Natural Language Symptom Extractor**: Normalizes free text input, removes special characters, and matches descriptions to a list of 131 symptoms.
* **Random Forest ML Classification**: Computes probability distributions for 41 different diseases, outputting the most likely condition and confidence metrics.
* **Top 3 Diagnostic Probabilities**: Computes and displays the top 3 alternative diagnoses in real time.
* **Weighted Severity Scoring**: Integrates a clinical database of symptom weights to score case severity and assign a Risk Level (Low, Medium, High).
* **Automated Follow-up Engine**: Identifies missing symptoms associated with the predicted disease and suggests relevant follow-up questions to help users narrow down their condition.
* **Instant Emergency Triaging**: Scans for life-threatening emergency symptoms (chest pain, breathlessness, unconsciousness, severe bleeding) and overrides standard output with warning directions.
* **Interactive Web Dashboard**: A glassmorphic split-pane web UI with custom circular SVG gauges, visual probability bar charts, and clickable suggestion chips.
* **CORS-Enabled & Local-First**: Secured API that runs locally on FastAPI and can be easily integrated into mobile or web frontends.

---

## ⚡ Technical Innovation & Data Integrity

1. **Normalized Machine Learning Model**: Resolved the original dataset spacing anomalies. In the original data, 130 out of 131 symptoms contained leading/trailing spaces (e.g., `' chest_pain'`, `' high_fever'`). This caused lookups to return `0` severity. The model is now trained on fully stripped, space-less variables, enabling perfect matches.
2. **Disease spelling matching**: Standardized spelling differences between data sources (e.g., mapping `'Dimorphic hemmorhoids(piles)'` and `'Diabetes '` to their clean equivalents) to prevent index lookup crashes.
3. **Safe Database Query fallbacks**: Built query checks that return fallback statements instead of crashing the Python server with `IndexError` when descriptions or precautions are missing.
4. **Symptom Typo Aliasing**: Programmed the parser to map common search keywords (like `"foul smell of urine"` to `"foul_smell_ofurine"`) to correctly identify user intent.

---

## ⚙️ How to Run Locally

### 1️⃣ Virtual Environment Setup
```powershell
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 2️⃣ Install Dependencies
```bash
pip install -r recquirements.txt
```

### 3️⃣ Retrain the Classifier (Creates models/disease_model.pkl)
```bash
python train_model.py
```

### 4️⃣ Start the Backend API (http://localhost:8000)
```bash
uvicorn main:app --reload
```

### 5️⃣ Run the Interactive Web Dashboard (http://localhost:8080)
```bash
python -m http.server 8080 --directory frontend
```
