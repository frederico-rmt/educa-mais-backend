import pytest
from src.domain.value_objects.email import Email
from src.domain.entities.user import User

def test_create_user():
  email = Email('teste@mail.com')
  user = User('João', email, 'coxinha123')
  assert user.name == 'João'
  assert user.email.value == 'teste@mail.com'
  assert user.password == 'coxinha123'

def test_create_with_wrong_email_instance():
  with pytest.raises(TypeError) as exc:
    User('João', 'errado@email.com', 'coxinha123')
  assert "email deve ser um objeto Email" in str(exc.value)

@pytest.mark.parametrize("invalid_password", [
  "",
  "    ",
  123456,
  None,
  [],
  True,
  {},
  object()
])
def test_create_with_wrong_password_instance(invalid_password):
  with pytest.raises(ValueError) as exc:
    User('João', Email('errado@email.com'), invalid_password)
  assert "eve passar uma senha válida" in str(exc.value)

def test_create_repr():
  email = Email('teste@mail.com')
  user = User('João', email, 'coxinha123')
  assert repr(user) == "name: João; email: teste@mail.com; senha: coxinha123"