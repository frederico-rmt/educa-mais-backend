from abc import ABC, abstractmethod
from typing import Any

class IAIDriver(ABC):
  @abstractmethod
  def generate_content(self, prompt: str, system_instruction: str, response_json_schema: dict[str, Any]):
    pass