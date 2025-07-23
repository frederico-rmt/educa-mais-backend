import time
from src.application.repository.discursive_question_repository import IDiscursiveQuestionRepository
from src.domain.entities.discursive_question import DiscursiveQuestion
from src.domain.value_objects.uuid_identifier import UuidIdentifier
from src.helpers.uuid_generator import UuidGenerator


class CreateDiscursiveQuestion():
  def __init__(self, question_repository: IDiscursiveQuestionRepository):
    self._question_repository = question_repository

  async def execute(self, id_author: str, title: str, prompt: str, expected_answer: str, criteria: str, tags: list[str], topic: str, difficulty, grade_level: str):
    uuid = UuidGenerator.generate()
    id = UuidIdentifier(uuid)
    author_identifier = UuidIdentifier(id_author)
    discursive_question = DiscursiveQuestion(id, author_identifier, title, prompt, expected_answer, criteria, tags, topic, difficulty, grade_level, time.time())
    await self._question_repository.save(discursive_question)
    return discursive_question.id.value
