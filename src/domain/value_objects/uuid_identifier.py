import uuid
import re

class UuidIdentifier:
  _UUID_REGEX = re.compile(
    r"^[a-f0-9]{8}-[a-f0-9]{4}-[1-5][a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$"
  )

  def __init__(self, value: str):
    if not self._UUID_REGEX.match(value):
      raise ValueError("Invalid uuid format")
    self.value = str(value)