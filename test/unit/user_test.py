import pytest
from src.helpers.uuid_generator import UuidGenerator
from src.domain.value_objects.uuid_identifier import UuidIdentifier
from src.domain.value_objects.email import Email
from src.domain.entities.user import User

def test_create_user():
  id = UuidIdentifier(UuidGenerator().generate())
  email = Email('teste@mail.com')
  user = User(id, 'João', email, 'coxinha123', 'teacher')
  assert user.id == id
  assert user.name == 'João'
  assert user.email.value == 'teste@mail.com'
  assert user.password == 'coxinha123'
  assert user.role == 'teacher'

@pytest.mark.parametrize("id, name, email, password, role, expected_error", [
  (None, "João", Email("joao@email.com"), "coxinha123", "teacher", "id must be an UuidIdentifier"),
  (UuidIdentifier(UuidGenerator().generate()), None, Email("joao@email.com"), "coxinha123", "teacher", "name is required"),
  (UuidIdentifier(UuidGenerator().generate()), "João", "errado@email.com", "coxinha123", "teacher", "email must be an Email"),
  (UuidIdentifier(UuidGenerator().generate()), "João", Email("joao@email.com"), "coxinha123", None, "role is required"),
])
def test_user_creation_with_invalid_fields(id, name, email, password, role, expected_error):
  with pytest.raises((TypeError, ValueError)) as exc:
    User(id, name, email, password, role)
  assert expected_error in str(exc.value)

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
    User(UuidIdentifier(UuidGenerator().generate()), 'João', Email('errado@email.com'), invalid_password, 'teacher')
  assert "password is required" in str(exc.value)