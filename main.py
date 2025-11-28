from fastapi import FastAPI, HTTPException
import os, requests

app = FastAPI()

API_KEY = os.getenv("API_KEY") #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" 
URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost",   # required field for OpenRouter policies
    # "X-Title": "Local Test Service"
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
