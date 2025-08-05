from src.application.repository.discursive_answer_repository import IDiscursiveAnswerRepository

class GetDiscursiveAnswer():
  def __init__(self, discursive_answer_repository: IDiscursiveAnswerRepository):
    self._discursive_answer_repository = discursive_answer_repository

  async def execute(self, id: str):
    discursive_answer = await self._discursive_answer_repository.get_answer(id)
    return discursive_answer