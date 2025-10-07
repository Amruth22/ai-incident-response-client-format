"""
Gemini AI Client - Utility Service
Interfaces with Google Gemini AI for incident analysis
"""

import logging
from typing import Dict, Any, Optional
import google.generativeai as genai
from config import get_config_value

logger = logging.getLogger("gemini_client")


class GeminiClient:
    """Gemini AI client utility - reusable across workflows"""
    
    def __init__(self):
        api_key = get_config_value("GEMINI_API_KEY", "")
        model_name = get_config_value("GEMINI_MODEL", "gemini-2.0-flash")
        
        if not api_key:
            logger.warning("Gemini API key not configured")
            self.model = None
        else:
            try:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel(model_name)
                logger.info(f"Gemini client initialized with model: {model_name}")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini: {e}")
                self.model = None
    
    def generate_content(self, prompt: str) -> str:
        """
        Generate content using Gemini
        
        Args:
            prompt: Prompt text
        
        Returns:
            Generated text response
        """
        if not self.model:
            raise Exception("Gemini API not available")
        
        response = self.model.generate_content(prompt)
        return response.text if hasattr(response, 'text') else str(response)
