import time
from src.application.repository.discursive_answer_repository import IDiscursiveAnswerRepository
from src.application.repository.discursive_question_repository import IDiscursiveQuestionRepository
from src.domain.entities.discursive_answer import DiscursiveAnswer
from src.infra.ai.question_ai_gateway import IQuestionAIGateway
from src.domain.value_objects.uuid_identifier import UuidIdentifier
from src.helpers.uuid_generator import UuidGenerator


class CreateDiscursiveAnswer():
  def __init__(self, question_repository: IDiscursiveQuestionRepository, discursive_answer_repository: IDiscursiveAnswerRepository, question_ai_gateway: IQuestionAIGateway):
    self._question_repository = question_repository
    self._discursive_answer_repository = discursive_answer_repository
    self._question_ai_gateway = question_ai_gateway

  async def execute(self, uuid_question: str, uuid_student: str, student_answer: str):
    uuid = UuidGenerator.generate()
    id_answer = UuidIdentifier(uuid)
    id_question = UuidIdentifier(uuid_question)
    id_student = UuidIdentifier(uuid_student)
    created_at = int(time.time())
    corrected_at = created_at

    discursive_question = await self._question_repository.get_question(uuid_question)

    feedback, grade = await self._question_ai_gateway.generate_discursive_question_feedback(discursive_question.prompt, discursive_question.expected_answer ,student_answer, discursive_question.criteria)

    answer = DiscursiveAnswer(
      id=id_answer,
      id_question=id_question,
      id_student=id_student,
      answer=student_answer,
      grade=grade,
      feedback=feedback,
      created_at=created_at,
      corrected_at=corrected_at
    )

    await self._discursive_answer_repository.save(answer)
    return {
      "id_answer": answer.id.value,
      "grade": grade,
      "feedback": feedback
    }