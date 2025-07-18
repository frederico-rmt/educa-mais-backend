class RawPassword:
  def __init__(self, value: str):
    self._is_valid(value)
    self._value = value

  def _is_valid(self, password: str):
    if not isinstance(password, str) or not password.strip():
      raise ValueError("Deve criar uma senha válida")
    if len(password) < 6 or len(password) > 12:
      raise ValueError("Deve possuir entre 6 e 12 caracteres")
    if not any (char.isupper() for char in password):
      raise ValueError("Deve conter ao menos uma letra maíuscula")
    if not any(char.isdigit() for char in password):
        raise ValueError("Deve conter ao menos um número")
    if not password.isalnum():
      raise ValueError("Deve conter apenas letras e números")

  def __str__(self):
    return self._value

  @property

  def value(self):
    return self._value