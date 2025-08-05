import time
from src.domain.value_objects.uuid_identifier import UuidIdentifier
from src.domain.entities.discursive_answer import DiscursiveAnswer
from src.application.repository.discursive_answer_repository import IDiscursiveAnswerRepository
from src.infra.database.database_driver import IDatabaseDriver


class DiscursiveAnswerSqlDatabase(IDiscursiveAnswerRepository):
  def __init__(self, database_driver: IDatabaseDriver):
    self._database_driver = database_driver
    self._table = "discursive_answers"
    self._schema = "educa_mais"

  async def save(self, discursive_answer: DiscursiveAnswer):
    print('discursive answer', discursive_answer.__dict__)
    query = f'INSERT INTO "{self._schema}"."{self._table}"(uuid, id_question, id_student, answer, grade, feedback, created_at, corrected_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
    await self._database_driver.query(query, [discursive_answer.id.value, discursive_answer.id_question.value, discursive_answer.id_student.value, discursive_answer.answer, discursive_answer.grade, discursive_answer.feedback, discursive_answer.created_at, discursive_answer.corrected_at])

  async def get_answer(self, id: str) -> DiscursiveAnswer:
    query = f'SELECT uuid, id_question, id_student, answer, grade, feedback, created_at, corrected_at FROM "{self._schema}"."{self._table}" WHERE uuid = %s'
    rows = await self._database_driver.query(query, [id])
    row = rows[0]
    return DiscursiveAnswer(
      id=UuidIdentifier(row[0]),
      id_question=UuidIdentifier(row[1]),
      id_student=UuidIdentifier(row[2]),
      answer=row[3],
      grade=row[4],
      feedback=row[5],
      created_at=row[6],
      corrected_at=row[7]
    )

  def get_answers(self, filters):
    return super().get_answers(filters)