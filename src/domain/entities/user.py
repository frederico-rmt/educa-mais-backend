from src.domain.value_objects.uuid_identifier import UuidIdentifier
from src.domain.value_objects.email import Email

class User:
  def __init__(self, id: UuidIdentifier, name: str, email: Email, password: str, role: str):
    if not isinstance(id, UuidIdentifier):
      raise TypeError("id must be an UuidIdentifier")
    if not isinstance(name, str) or not name.strip():
      raise ValueError("name is required")
    if not isinstance(email, Email):
      raise TypeError("email must be an Email")
    if not isinstance(password, str) or not password.strip():
      raise ValueError("password is required")
    if not isinstance(role, str) or not role.strip():
      raise ValueError("role is required")
    self.id = id
    self.name = name
    self.email = email
    self.password = password
    self.role = role