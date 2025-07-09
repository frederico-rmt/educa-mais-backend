from app.domain.value_objects.email import Email

class User:
  def __init__(self, email: Email, password: str):
    if not isinstance(email, Email):
      raise TypeError("email deve ser um objeto Email")
    if not isinstance(password, str) or not password.strip():
      raise ValueError("deve passar uma senha válida")
    self.email = email
    self.password = password

  def __repr__(self):
    return f"email: {self.email.value}; senha: {self.password}"