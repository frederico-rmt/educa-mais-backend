import pytest
from src.domain.value_objects.email import Email

@pytest.mark.parametrize("valid_email", [
    "teste@dominio.com",
    "usuario@mail.org",
    "nome.sobrenome@empresa.com.br",
    "abc@xyz.co"
])
def test_email_valido(valid_email):
    email = Email(valid_email)
    assert email.value == valid_email
    assert str(email) == valid_email

@pytest.mark.parametrize("invalid_email", [
    "semarroba.com",
    "invalido@",
    "@dominio.com",
    "",
    "   ",
    "nome@.com"
])
def test_email_invalido(invalid_email):
    with pytest.raises(ValueError) as exc:
        Email(invalid_email)
    assert "Email inválido" in str(exc.value)

def test_emails_comparacao_case_insensitive():
    assert Email("User@Email.com") == Email("user@email.com")