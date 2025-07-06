import requests
import time

OLLAMA_API_URL = "http://localhost:11434/api/generate"  # Adjust if needed

def call_llm(prompt, model="phi3:mini", max_retries=3):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.post(OLLAMA_API_URL, json=payload, timeout=60)
            response.raise_for_status()
            return response.json()["response"]
        except requests.exceptions.ConnectionError:
            if attempt < max_retries - 1:
                print(f"⚠️  Connection failed, retrying in 2 seconds... (attempt {attempt + 1}/{max_retries})")
                time.sleep(2)
            else:
                raise Exception("Failed to connect to Ollama. Make sure Ollama is running on localhost:11434")
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                print(f"⚠️  Request timeout, retrying... (attempt {attempt + 1}/{max_retries})")
                time.sleep(1)
            else:
                raise Exception("LLM request timed out")
        except Exception as e:
            raise Exception(f"LLM API error: {e}")