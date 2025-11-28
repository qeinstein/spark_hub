from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os, requests
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("API_KEY")
URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://openrouter.ai",
    "X-Title": "Public AI Proxy"
}

class AskRequest(BaseModel):
    user_input: str

@app.post("/ask")
def ask(req: AskRequest):
    payload = {
        "model": "mistralai/mistral-small-3.1-24b-instruct:free",
        "messages": [
            { "role": "system", "content": "You're an educational assistant, reply in the same language the user sent the message in." },
            { "role": "user", "content": req.user_input }
        ],
        "temperature": 0.3
    }

    if not API_KEY:
        raise HTTPException(status_code=500, detail="API_KEY not set")

    resp = requests.post(URL, headers=HEADERS, json=payload)
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)

    return {"response": resp.json()["choices"][0]["message"]["content"]}
