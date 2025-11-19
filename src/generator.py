import time
from abc import ABC, abstractmethod
from .config import Config, LLMProvider

class LLMGenerator(ABC):
    @abstractmethod
    def generate(self, prompt: str, max_tokens: int = 2000) -> str:
        pass

class MockGenerator(LLMGenerator):
    def generate(self, prompt: str, max_tokens: int = 2000) -> str:
        print(f"[MockGenerator] Generating response for prompt: {prompt[:50]}...")
        time.sleep(0.5) # Simulate latency
        
        if "idea" in prompt.lower():
            return "A story about a space gardener who discovers a plant that eats time."
        elif "outline" in prompt.lower():
            # Return a simple mock outline format
            return """
            Chapter 1: The Discovery
            - Scene 1: Finding the seed
            - Scene 2: Planting it
            
            Chapter 2: The Growth
            - Scene 1: First sprout
            - Scene 2: Time skips
            """
        else:
            # Generate dummy text
            return "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 50

class GeminiGenerator(LLMGenerator):
    def __init__(self, api_key: str, model_name: str):
        self.api_key = api_key
        self.model_name = model_name
        import requests
        self.requests = requests
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        
    def generate(self, prompt: str, max_tokens: int = 8192) -> str:
        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "maxOutputTokens": max_tokens
            }
        }
        
        try:
            response = self.requests.post(self.url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            if 'candidates' in result and result['candidates']:
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                print(f"Unexpected response format: {result}")
                return ""
        except Exception as e:
            print(f"Error generating content: {e}")
            if 'response' in locals():
                 print(f"Response Status: {response.status_code}")
                 print(f"Response Text: {response.text}")
            return ""

class GeminiFlashGenerator(LLMGenerator):
    """Ultra-fast Gemini 1.5 Flash for production speed"""
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.model_name = "gemini-1.5-flash"
        import requests
        self.requests = requests
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={api_key}"
        
    def generate(self, prompt: str, max_tokens: int = 8192) -> str:
        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "maxOutputTokens": max_tokens,
                "temperature": 0.7,
                "topP": 0.95,
                "topK": 40
            }
        }
        
        try:
            response = self.requests.post(self.url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            if 'candidates' in result and result['candidates']:
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                print(f"Unexpected response format: {result}")
                return ""
        except Exception as e:
            print(f"Error generating content: {e}")
            if 'response' in locals():
                 print(f"Response Status: {response.status_code}")
                 print(f"Response Text: {response.text}")
            return ""


class DeepSeekGenerator(LLMGenerator):
    def __init__(self, api_key: str, model_name: str):
        self.api_key = api_key
        self.model_name = model_name
        import requests
        self.requests = requests
        self.url = "https://api.deepseek.com/chat/completions"
        
    def generate(self, prompt: str, max_tokens: int = 4000) -> str:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        data = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": "You are a helpful academic assistant."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": 0.7
        }
        
        try:
            response = self.requests.post(self.url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        except Exception as e:
            print(f"Error generating content: {e}")
            if 'response' in locals():
                 print(f"Response Status: {response.status_code}")
                 print(f"Response Text: {response.text}")
            return ""

def get_generator(config: Config) -> LLMGenerator:
    if config.PROVIDER == LLMProvider.MOCK:
        return MockGenerator()
    elif config.PROVIDER == LLMProvider.GEMINI:
        return GeminiGenerator(config.API_KEY, config.MODEL_NAME)
    elif config.PROVIDER == LLMProvider.GEMINI_FLASH:
        return GeminiFlashGenerator(config.API_KEY)
    elif config.PROVIDER == LLMProvider.DEEPSEEK:
        return DeepSeekGenerator(config.API_KEY, config.MODEL_NAME)
    else:
        raise ValueError(f"Unsupported provider: {config.PROVIDER}")

