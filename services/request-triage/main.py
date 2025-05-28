from fastapi import FastAPI, Request, Header
from pydantic import BaseModel
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

class TriageRequest(BaseModel):
    description: str
    location: str
    user_id: str

@app.post("/analyze")
async def analyze_request(payload: TriageRequest, authorization: str = Header(...)):
    prompt = f"Emergency reported: {payload.description}. Location: {payload.location}. What type of emergency is this and how urgent is it from 1 to 10?"
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Dummy parse
    emergency_type = "Medical"
    urgency = 9

    # Store in Supabase (pseudo)
    # supabase.table("requests").insert({...})

    return {
        "type": emergency_type,
        "urgency": urgency,
        "status": "pending"
    }
