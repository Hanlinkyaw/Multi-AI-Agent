import os
import google.generativeai as genai
from typing import Optional

class GeminiModel:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini model with API key.
        Uses available model for compatibility.
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is required")
        
        genai.configure(api_key=self.api_key)
        
        # List available models first
        try:
            models = genai.list_models()
            available_models = [model.name.split('/')[-1] for model in models if 'generateContent' in model.supported_generation_methods]
            print(f"Available models: {available_models}")
            
            # Try the first available model
            if available_models:
                self.model = genai.GenerativeModel(available_models[0])
                self.model_name = available_models[0]
            else:
                raise ValueError("No compatible models found")
                
        except Exception as e:
            raise ValueError(f"Failed to initialize Gemini model: {e}")
    
    def get_model(self) -> genai.GenerativeModel:
        """Get the initialized Gemini model."""
        return self.model
    
    def get_model_name(self) -> str:
        """Get the name of the currently used model."""
        return self.model_name
    
    def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate a response from the Gemini model."""
        try:
            response = self.model.generate_content(prompt, **kwargs)
            return response.text
        except Exception as e:
            raise RuntimeError(f"Failed to generate response: {e}")
