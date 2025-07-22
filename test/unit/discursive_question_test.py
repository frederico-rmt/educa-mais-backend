import time
import pytest
from src.domain.entities.discursive_question import DiscursiveQuestion
from src.domain.value_objects.uuid_identifier import UuidIdentifier
from src.helpers.uuid_generator import UuidGenerator


def test_create_discursive_question():
  id=UuidIdentifier(UuidGenerator().generate())
  authorId=UuidIdentifier(UuidGenerator().generate())
  title="A causa da Primeira Guerra Mundial"
  prompt="Explique as principais causas que levaram ao início da Primeira Guerra Mundial."
  expected_answer="As principais causas incluem o assassinato do arquiduque Franz Ferdinand, alianças militares, nacionalismo exacerbado e corrida armamentista."
  criteria="Responder ao menos três causas e explicar o contexto de cada uma."
  tags=["world war" "europe"]
  topic="history"
  difficulty="medium"
  grade_level=9
  created_at=time.time()
  question = DiscursiveQuestion(id, authorId, title, prompt, expected_answer, criteria, tags, topic, difficulty, grade_level, created_at)
  assert question.id == id
  assert question.authorId == authorId
  assert question.title == title
  assert question.prompt == prompt
  assert question.expected_answer == expected_answer
  assert question.criteria == criteria
  assert question.tags == tags
  assert question.topic == topic
  assert question.difficulty == difficulty
  assert question.grade_level == grade_level

@pytest.mark.parametrize("field,value,error_message", [
    ("id", "string", "id must be an UuidIdentifier"),
    ("authorId", None, "authorId must be an UuidIdentifier"),
    ("title", "", "title is required"),
    ("prompt", "", "prompt is required"),
    ("expected_answer", "", "expected_answer is required"),
    ("criteria", "", "criteria is required"),
    ("tags", [], "tags must be a non-empty list"),
    ("topic", "", "topic is required"),
    ("difficulty", "", "difficulty is required"),
    ("grade_level", None, "grade_level is required"),
    ("created_at", None, "created_at is required"),
])
def test_create_discursive_question_failure(field, value, error_message):
    valid_data = {
        "id": UuidIdentifier(UuidGenerator.generate()),
        "authorId": UuidIdentifier(UuidGenerator.generate()),
        "title": "A causa da Primeira Guerra Mundial",
        "prompt": "Explique as principais causas que levaram ao início da Primeira Guerra Mundial.",
        "expected_answer": "As principais causas incluem o assassinato do arquiduque Franz Ferdinand...",
        "criteria": "Responder ao menos três causas e explicar o contexto de cada uma.",
        "tags": ["world war", "europe"],
        "topic": "history",
        "difficulty": "medium",
        "grade_level": 9,
        "created_at": time.time()
    }
    valid_data[field] = value
    with pytest.raises(ValueError) as exc:
        DiscursiveQuestion(**valid_data)
    assert error_message in str(exc.value)