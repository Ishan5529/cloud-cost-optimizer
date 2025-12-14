import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_API_TOKEN = os.getenv("HF_API_TOKEN")

API_URL = "https://router.huggingface.co/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {HF_API_TOKEN}",
    "Content-Type": "application/json"
}

# MODEL_NAME = "HuggingFaceH4/zephyr-7b-beta:featherless-ai"
MODEL_NAME = "meta-llama/Llama-3.1-8B-Instruct:novita"

def call_llm(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a JSON generator. "
                    "You must output exactly one valid JSON object and nothing else. "
                    "Do not ask questions. Do not include explanations. "
                    "Do not continue the conversation."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2,
        "top_p": 0.9,
        "max_tokens": 1200
    }

    response = requests.post(
        API_URL,
        headers=HEADERS,
        json=payload,
        timeout=90
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"HF API Error {response.status_code}: {response.text}"
        )

    data = response.json()

    try:
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError) as e:
        raise ValueError(f"Unexpected HF response format: {data}") from e
