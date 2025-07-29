from typing import Any, Dict
import json
from google import genai
from google.genai import types
from src.infra.ai.ai_driver import IAIDriver

class GoogleGenAIDriver(IAIDriver):
  def __init__(self, api_key: str, ai_model: str):
    self._api_key = api_key
    self._ai_model = ai_model
    self._client = genai.Client(api_key=self._api_key)

  async def generate_content(self, prompt: str, system_instruction: str, response_json_schema):
    response = self._client.models.generate_content(
      model=self._ai_model,
      contents=prompt,
      config=types.GenerateContentConfig(
        system_instruction=system_instruction,
        response_json_schema=response_json_schema,
        response_mime_type="application/json"
      )
    )
    json_response = response.text
    return json.loads(json_response)