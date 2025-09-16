from fastapi import APIRouter
from pydantic import BaseModel
import prompt

router = APIRouter()

class RequestData(BaseModel):
    text: str

@router.post("/analyze")
def analyze(data: RequestData):
    """
    API endpoint to analyze text using prompt.py logic.
    """
    result = prompt.analyze_text(data.text)
    return {"input": data.text, "output": result}

@router.get("/health")
def health_check():
    return {"status": "ok"}
