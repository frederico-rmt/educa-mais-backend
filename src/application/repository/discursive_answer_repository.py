from abc import ABC, abstractmethod
from src.domain.entities.discursive_answer import DiscursiveAnswer

class IDiscursiveAnswerRepository(ABC):
  @abstractmethod
  def save(self, discursive_answer: DiscursiveAnswer):
    pass

  @abstractmethod
  def get_answer(self, id: str):
    pass

  @abstractmethod
  def get_answers(self, filters: str):
    pass