from abc import ABC, abstractmethod
from src.domain.entities.discursive_question import DiscursiveQuestion

class IDiscursiveQuestionRepository(ABC):
  @abstractmethod
  def save(self, discursive_question: DiscursiveQuestion):
    pass

  @abstractmethod
  def get_question(self, id: str):
    pass

  @abstractmethod
  def get_questions(self, filters: str):
    pass
