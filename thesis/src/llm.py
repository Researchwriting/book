import requests
import json
from .config import Config

class LLMClient:
    def __init__(self):
        self.api_key = Config.DEEPSEEK_API_KEY
        self.model = Config.MODEL_NAME
        self.api_url = "https://api.deepseek.com/v1/chat/completions"

    def generate(self, prompt, system_prompt="You are a helpful academic assistant.", max_tokens=4096):
        """
        Generate text using DeepSeek API.
        """
        if not self.api_key:
            return "Error: No DeepSeek API key configured."

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": 0.7
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                print(f"Error calling DeepSeek API: {response.status_code} - {response.text}")
                return f"Error: API call failed with status {response.status_code}"
        except Exception as e:
            print(f"Exception calling LLM: {e}")
            return f"Error: {str(e)}"
