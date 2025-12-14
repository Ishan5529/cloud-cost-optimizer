import json
import time

MAX_RETRIES = 3

def safe_llm_call(llm_func, prompt: str):
    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            raw = llm_func(prompt)
            parsed = json.loads(raw.strip())
            return parsed

        except Exception as e:
            print(f"[Retry {attempt}/{MAX_RETRIES}] LLM error: {e}")
            last_error = e
            time.sleep(2)

    raise RuntimeError("LLM failed after 3 attempts") from last_error
