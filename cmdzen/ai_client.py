"""OpenRouter API client for AI-powered error analysis."""

import json
import time
import requests
from typing import Optional, Dict, Any

from .config import Config
from .prompts import create_messages


class OpenRouterClient:
    """Client for interacting with OpenRouter API."""
    
    def __init__(self):
        """Initialize the OpenRouter client."""
        Config.validate()
        self.api_url = Config.OPENROUTER_API_URL
        self.headers = Config.get_headers()
        self.model = Config.DEFAULT_MODEL
        self.timeout = Config.REQUEST_TIMEOUT
        self.max_retries = Config.MAX_RETRIES
    
    def analyze_error(self, error_or_issue: str) -> str:
        """
        Analyze an error or system issue using AI.
        
        Args:
            error_or_issue: The error message, command output, or problem description
            
        Returns:
            AI-generated solution and explanation
            
        Raises:
            Exception: If the API request fails after retries
        """
        messages = create_messages(error_or_issue)
        
        payload = {
            "model": self.model,
            "messages": messages
        }
        
        response_data = self._make_request(payload)
        
        # Extract the assistant's response
        if "choices" in response_data and len(response_data["choices"]) > 0:
            return response_data["choices"][0]["message"]["content"]
        else:
            raise Exception("Unexpected API response format")
    
    def _make_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make an HTTP request to the OpenRouter API with retry logic.
        
        Args:
            payload: The request payload
            
        Returns:
            API response data
            
        Raises:
            Exception: If all retry attempts fail
        """
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    url=self.api_url,
                    headers=self.headers,
                    data=json.dumps(payload),
                    timeout=self.timeout
                )
                
                if response.status_code == 401:
                    raise Exception(
                        "Authentication failed. Please check your OPENROUTER_API_KEY."
                    )
                elif response.status_code == 429:
                    wait_time = 2 ** attempt  # Exponential backoff
                    if attempt < self.max_retries - 1:
                        time.sleep(wait_time)
                        continue
                    raise Exception(
                        "Rate limit exceeded. Please try again later or upgrade your API plan."
                    )
                elif response.status_code >= 500:
                    if attempt < self.max_retries - 1:
                        time.sleep(1)
                        continue
                    raise Exception(
                        f"OpenRouter API server error (status {response.status_code}). "
                        "Please try again later."
                    )
                
                response.raise_for_status()
                return response.json()
                
            except requests.exceptions.Timeout:
                last_error = Exception(
                    f"Request timed out after {self.timeout} seconds. "
                    "Please check your internet connection and try again."
                )
                if attempt < self.max_retries - 1:
                    time.sleep(1)
                    continue
                    
            except requests.exceptions.ConnectionError:
                last_error = Exception(
                    "Failed to connect to OpenRouter API. "
                    "Please check your internet connection."
                )
                if attempt < self.max_retries - 1:
                    time.sleep(1)
                    continue
                    
            except requests.exceptions.RequestException as e:
                last_error = Exception(f"API request failed: {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(1)
                    continue
        
        raise last_error or Exception("API request failed after all retries")
