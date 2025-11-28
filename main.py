from fastapi import FastAPI, HTTPException
import os, requests
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

API_KEY = os.getenv("API_KEY")
URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://openrouter.ai",
    "X-Title": "Public AI"
}

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


that is my cpde
