"""Configuration management for cmd-zen."""

import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Config:
    """Application configuration."""
    
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
    
    DEFAULT_MODEL = "deepseek/deepseek-r1-0528:free"
    
    SITE_URL = os.getenv("SITE_URL", "")
    SITE_NAME = os.getenv("SITE_NAME", "cmd-zen")
    
    REQUEST_TIMEOUT = 30
    MAX_RETRIES = 3
    
    @classmethod
    def validate(cls):
        """Validate required configuration."""
        if not cls.OPENROUTER_API_KEY:
            raise ValueError(
                "OPENROUTER_API_KEY not found in environment variables. "
                "Please set it in your .env file or export it as an environment variable."
            )
        
        if cls.OPENROUTER_API_KEY == "your_api_key_here":
            raise ValueError(
                "Please replace 'your_api_key_here' with your actual OpenRouter API key "
                "in the .env file."
            )
    
    @classmethod
    def get_headers(cls):
        """Get HTTP headers for OpenRouter API requests."""
        headers = {
            "Authorization": f"Bearer {cls.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }
        
        if cls.SITE_URL:
            headers["HTTP-Referer"] = cls.SITE_URL
        
        if cls.SITE_NAME:
            headers["X-Title"] = cls.SITE_NAME
        
        return headers
