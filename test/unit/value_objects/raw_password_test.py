import pytest
from app.domain.value_objects.raw_password import RawPassword

@pytest.mark.parametrize("valid_password", [
  "Senha123456"
])
def test_create_valid_password(valid_password):
  password = RawPassword(valid_password)
  assert password.value == valid_password

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
def test_invalid_password_type(invalid_password):
  with pytest.raises(ValueError) as exc:
    RawPassword(invalid_password)
  assert "Deve criar uma senha válida" in str(exc.value)

@pytest.mark.parametrize("invalid_password", [
  "aaaaaa11"
])
def test_password_without_uppercase(invalid_password):
  with pytest.raises(ValueError) as exc:
    RawPassword(invalid_password)
  assert "Deve conter ao menos uma letra maíuscula" in str(exc.value)

@pytest.mark.parametrize("invalid_password", [
  "AAAAAAAA"
])
def test_password_without_number(invalid_password):
  with pytest.raises(ValueError) as exc:
    RawPassword(invalid_password)
  assert "Deve conter ao menos um número" in str(exc.value)

@pytest.mark.parametrize("invalid_password", [
  "A1",
  "AAAAAAA1111111"
])
def test_password_between_6_and_12(invalid_password):
  with pytest.raises(ValueError) as exc:
    RawPassword(invalid_password)
  assert "Deve possuir entre 6 e 12 caracteres" in str(exc.value)

@pytest.mark.parametrize("invalid_password", [
  "A1!!!!!!!!!"
])
def test_password_between_6_and_12(invalid_password):
  with pytest.raises(ValueError) as exc:
    RawPassword(invalid_password)
  assert "Deve conter apenas letras e números" in str(exc.value)