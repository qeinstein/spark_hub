

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
import os, requests
from dotenv import load_dotenv


app = FastAPI()

load_dotenv()

API_KEY = os.getenv("API_KEY")
URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://openrouter.ai",  # required by OpenRouter
    "X-Title": "Public AI Proxy"
}
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ask")
def ask(user_input: str):
    payload = {
        "model": "mistralai/mistral-small-3.1-24b-instruct:free",
        "messages": [
            { "role": "system", "content": "You're an educational assistant, reply in the same language the user sent the message in." },
            { "role": "user", "content": user_input }
        ],
        "temperature": 0.3
    }

    resp = requests.post(URL, headers=HEADERS, json=payload)

    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)

    data = resp.json()
    return {
        "response": data["choices"][0]["message"]["content"]
    }

