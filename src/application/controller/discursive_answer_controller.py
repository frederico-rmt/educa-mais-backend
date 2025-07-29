from src.application.repository.discursive_question_repository import IDiscursiveQuestionRepository
from src.infra.ai.question_ai_gateway import IQuestionAIGateway
from src.application.repository.discursive_answer_repository import IDiscursiveAnswerRepository
from src.application.usecase.create_discursive_answer import CreateDiscursiveAnswer
from src.application.usecase.get_discursive_answer import GetDiscursiveAnswer

class DiscursiveAnswerController:
  def __init__(self, http_server, discursive_answer_database: IDiscursiveAnswerRepository, discursive_question_database: IDiscursiveQuestionRepository, discursive_question_ai_gateway: IQuestionAIGateway):
    self._discursive_answer_database = discursive_answer_database
    self._discursive_question_database = discursive_question_database
    self._discursive_question_ai_gateway = discursive_question_ai_gateway

    http_server.register('post', '/answers/discursive-answers', self._create_discursive_answer())
    http_server.register('get', '/answers/discursive-answers/{id}', self._get_discursive_answer())

  def _create_discursive_answer(self):
    async def handler(headers, query, params, body):
      id_student = body['id_student']
      id_question = body['id_question']
      answer = body['answer']
      create_discursive_answer = CreateDiscursiveAnswer(self._discursive_question_database, self._discursive_answer_database, self._discursive_question_ai_gateway)
      ai_feedback = await create_discursive_answer.execute(id_question, id_student, answer)
      return {
        "id_answer": ai_feedback["id_answer"],
        "grade": ai_feedback["grade"],
        "feedback": ai_feedback["feedback"]
      }
    return handler

  def _get_discursive_answer(self):
    async def handler(headers, query, params, body):
      print('params', params)
      id = params['id']
      get_discursive_answer = GetDiscursiveAnswer(self._discursive_answer_database)
      discursive_answer = await get_discursive_answer.execute(id)
      discursive_answer_dto = {
        "id": discursive_answer.id.value,
        "id_question": discursive_answer.id_question.value,
        "id_student": discursive_answer.id_student.value,
        "answer": discursive_answer.answer,
        "grade": discursive_answer.grade,
        "feedback": discursive_answer.feedback,
        "created_at": discursive_answer.created_at,
        "corrected_at": discursive_answer.corrected_at
      }
      return discursive_answer_dto
    return handler
