import pytest
from src.domain.value_objects.uuid_identifier import UuidIdentifier

def test_should_create_identifier_with_valid_uuid():
  valid_uuid = "9a0a6060-138d-48d0-a585-9c8e8a4b92ac"
  identifier = UuidIdentifier(valid_uuid)
  assert identifier is not None
  assert identifier.value == valid_uuid

def test_should_throw_error_for_invalid_uuid():
  invalid_uuid = "9a0a6060-138d-48d0-a585-9c8e8a4b92a"  # inválido, último caractere removido
  with pytest.raises(ValueError, match="Invalid uuid"):
    UuidIdentifier(invalid_uuid)