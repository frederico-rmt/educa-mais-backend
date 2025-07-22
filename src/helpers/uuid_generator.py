import uuid

class UuidGenerator:
  @staticmethod
  def generate() -> str:
    return str(uuid.uuid4())