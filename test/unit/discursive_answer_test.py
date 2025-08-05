from src.domain.value_objects.uuid_identifier import UuidIdentifier
from src.helpers.uuid_generator import UuidGenerator
from src.domain.entities.discursive_answer import DiscursiveAnswer

def test_should_create_discursive_answer():
  id_answer=UuidIdentifier(UuidGenerator.generate())
  id_question=UuidIdentifier(UuidGenerator.generate())
  id_student=UuidIdentifier(UuidGenerator.generate())
  answer = DiscursiveAnswer(
    id=id_answer,
    id_question=id_question,
    id_student=id_student,
    answer="A resposta do aluno.",
    grade=9.5,
    feedback="Muito bom!",
    created_at=1721400000,
    corrected_at=1721400500
  )

  assert answer.id == id_answer
  assert answer.id_question == id_question
  assert answer.id_student == id_student
  assert answer.grade == 9.5
  assert answer.feedback == "Muito bom!"
  assert answer.corrected_at == 1721400500

import pytest
from src.domain.entities.discursive_answer import DiscursiveAnswer

@pytest.mark.parametrize("field, value, expected_error", [
  ("id", "invalid", "id must be an UuidIdentifier"),
  ("id_question", "invalid", "id_question must be an UuidIdentifier"),
  ("id_student", "invalid", "id_student must be an UuidIdentifier"),
  ("answer", "", "answer is required"),
  ("created_at", None, "created_at is required"),
])
def test_should_fail_on_invalid_fields(field, value, expected_error):
  valid_data = {
    "id": UuidIdentifier(UuidGenerator.generate()),
    "id_question": UuidIdentifier(UuidGenerator.generate()),
    "id_student": UuidIdentifier(UuidGenerator.generate()),
    "answer": "resposta válida",
    "grade": None,
    "feedback": None,
    "created_at": 1721400000,
    "corrected_at": None
  }

  valid_data[field] = value

  with pytest.raises(ValueError, match=expected_error):
    DiscursiveAnswer(**valid_data)
