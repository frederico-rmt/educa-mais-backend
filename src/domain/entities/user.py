from src.domain.value_objects.email import Email

class User:
  def __init__(self, name: str, email: Email, password: str, role: str):
    if not isinstance(name, str) or not name.strip():
      raise ValueError("Deve passar um nome válido")
    if not isinstance(email, Email):
      raise TypeError("email deve ser um objeto Email")
    if not isinstance(password, str) or not password.strip():
      raise ValueError("Deve passar uma senha válida")
    if not isinstance(role, str) or not role.strip():
      raise ValueError("Deve passar uma função válida")
    self.name = name
    self.email = email
    self.password = password
    self.role = role