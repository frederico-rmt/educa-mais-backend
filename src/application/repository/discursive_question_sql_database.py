import time
from src.domain.value_objects.uuid_identifier import UuidIdentifier
from src.application.repository.discursive_question_repository import IDiscursiveQuestionRepository
from src.domain.entities.discursive_question import DiscursiveQuestion
from src.infra.database.database_driver import IDatabaseDriver

class DiscursiveQuestionSqlDatabase(IDiscursiveQuestionRepository):
  def __init__(self, database_driver: IDatabaseDriver):
    self._database_driver = database_driver
    self._table = 'discursive_questions'
    self._schema = 'educa_mais'

  async def save(self, discursive_question: DiscursiveQuestion):
    query = f'INSERT INTO "{self._schema}"."{self._table}" (uuid, id_author, title, prompt, expected_answer, criteria, tags, topic, difficulty, grade_level, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    await self._database_driver.query(query, [discursive_question.id.value, discursive_question.id_author.value, discursive_question.title, discursive_question.prompt, discursive_question.expected_answer, discursive_question.criteria, discursive_question.tags, discursive_question.topic, discursive_question.difficulty, discursive_question.grade_level, discursive_question.created_at])

  async def get_question(self, id: str):
    query = f'SELECT uuid, id_author, title, prompt, expected_answer, criteria, tags, topic, difficulty, grade_level, created_at FROM "{self._schema}"."{self._table}" WHERE uuid = %s'
    row = await self._database_driver.query(query, [id])
    question_data = row[0]
    id_question = UuidIdentifier(question_data[0])
    id_author = UuidIdentifier(question_data[1])
    title = question_data[2]
    prompt = question_data[3]
    expected_answer = question_data[4]
    criteria = question_data[5]
    tags = question_data[6]
    topic = question_data[7]
    difficulty = question_data[8]
    grade_level = int(question_data[9])
    created_at = question_data[10]
    discursive_question = DiscursiveQuestion(id_question, id_author, title, prompt, expected_answer, criteria, tags, topic, difficulty, grade_level, created_at)
    return discursive_question

  async def get_questions(self, filters):
    return super().get_questions(filters)