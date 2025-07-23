from src.application.repository.discursive_question_repository import IDiscursiveQuestionRepository
from src.infra.authenticator.authenticator import IAuthenticator
from src.infra.hasher.hasher import IHasher
from src.application.usecase.login import Login
from src.application.usecase.create_discursive_question import CreateDiscursiveQuestion
from src.application.usecase.get_discursive_question import GetDiscursiveQuestion

class DiscursiveQuestionController:
  def __init__(self, http_server, discursive_question_database: IDiscursiveQuestionRepository):
    self._discursive_question_database = discursive_question_database

    http_server.register('post', '/questions/discursive-questions', self._create_discursive_question())
    http_server.register('get', '/questions/discursive-questions/{id}', self._get_discursive_question())

  def _create_discursive_question(self):
    async def handler(headers, query, params, body):
      id_author = body['id_author']
      title = body['title']
      prompt = body['prompt']
      expected_answer = body['expected_answer']
      criteria = body['criteria']
      tags = body['tags']
      topic = body['topic']
      difficulty = body['difficulty']
      grade_level = body['grade_level']
      create_discursive_question = CreateDiscursiveQuestion(self._discursive_question_database)
      id = await create_discursive_question.execute(id_author, title, prompt, expected_answer, criteria, tags, topic, difficulty, grade_level)
      return {'id': id}
    return handler

  def _get_discursive_question(self):
    async def handler(headers, query, params, body):
      id = params['id']
      get_discursive_question = GetDiscursiveQuestion(self._discursive_question_database)
      discursive_question = await get_discursive_question.execute(id)
      discursive_question_dto = {
        "id": discursive_question.id.value,
        "id_author": discursive_question.id_author.value,
        "title": discursive_question.title,
        "prompt": discursive_question.prompt,
        "expected_answer": discursive_question.expected_answer,
        "criteria": discursive_question.criteria,
        "tags": discursive_question.tags,
        "topic": discursive_question.topic,
        "difficulty": discursive_question.difficulty,
        "grade_level": discursive_question.grade_level,
        "created_at": discursive_question.created_at,
      }
      return discursive_question_dto
    return handler