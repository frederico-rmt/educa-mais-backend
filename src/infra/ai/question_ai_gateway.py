from abc import ABC, abstractmethod

class IQuestionAIGateway(ABC):
  @abstractmethod
  def generate_discursive_question_feedback(self, question: str, expected_answer: str, answer: str):
    pass