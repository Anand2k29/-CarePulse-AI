from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import logging

from services.ml_predictor import MLPredictor
from services.symptom_parser import SymptomParser
from services.severity_engine import SeverityEngine
from services.emergency import check_emergency
from services.followup_engine import FollowUpEngine
from services.formatter import ResponseFormatter

# ---------------------------------------------------
# Logging
# ---------------------------------------------------
logging.basicConfig(level=logging.INFO)

# ---------------------------------------------------
# App Initialization
# ---------------------------------------------------
app = FastAPI(title="Advanced AI Medical Chatbot API")

# Enable CORS (IMPORTANT for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------
# Initialize Services
# ---------------------------------------------------
predictor = MLPredictor()
severity_engine = SeverityEngine()
formatter = ResponseFormatter()
followup = FollowUpEngine()
parser = SymptomParser(predictor.symptom_list)

# ---------------------------------------------------
# Request / Response Models
# ---------------------------------------------------

class ChatRequest(BaseModel):
    message: str


class TopPrediction(BaseModel):
    Disease: str
    Probability_percent: float


class ChatResponse(BaseModel):
    Possible_Condition: str
    Matched_Symptoms: List[str]
    Description: str
    Recommended_Precautions: List[str]
    Risk_Level: str
    Severity_Score: int
    Confidence_percent: float
    Top_3_Predictions: List[TopPrediction]
    Follow_up_Questions: List[str]
    Emergency: bool
    Disclaimer: str


# ---------------------------------------------------
# Health Check Endpoint
# ---------------------------------------------------

@app.get("/")
def health_check():
    return {"status": "Medical Chatbot API is running"}


# ---------------------------------------------------
# Chat Endpoint
# ---------------------------------------------------

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        message = request.message
        logging.info(f"User input: {message}")

        parsed_symptoms = parser.parse(message)

        if len(parsed_symptoms) == 0:
            raise HTTPException(
                status_code=400,
                detail="No recognizable symptoms found. Please describe symptoms clearly."
            )

        if check_emergency(parsed_symptoms):
            return ChatResponse(
                Possible_Condition="Emergency Condition",
                Matched_Symptoms=parsed_symptoms,
                Description="This may indicate a medical emergency.",
                Recommended_Precautions=["Seek immediate medical attention"],
                Risk_Level="High",
                Severity_Score=0,
                Confidence_percent=95.0,
                Top_3_Predictions=[],
                Follow_up_Questions=[],
                Emergency=True,
                Disclaimer="This is not a medical diagnosis. Please consult a qualified doctor."
            )

        disease, confidence, top3 = predictor.predict(parsed_symptoms)

        severity_score = severity_engine.calculate_score(parsed_symptoms)
        risk_level = severity_engine.get_risk_level(severity_score)

        followup_questions = followup.suggest_followup(disease, parsed_symptoms)

        response_data = formatter.format(
            disease,
            risk_level,
            severity_score,
            parsed_symptoms,
            confidence,
            top3
        )

        response_data["Follow_up_Questions"] = followup_questions
        response_data["Emergency"] = False

        return response_data

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")