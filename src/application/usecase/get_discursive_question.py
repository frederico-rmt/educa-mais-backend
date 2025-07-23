from src.application.repository.discursive_question_repository import IDiscursiveQuestionRepository

class GetDiscursiveQuestion():
  def __init__(self, discursive_question_repository: IDiscursiveQuestionRepository):
    self._discursive_question_repository = discursive_question_repository

  async def execute(self, id: str):
    discursive_question = await self._discursive_question_repository.get_question(id)
    return discursive_question