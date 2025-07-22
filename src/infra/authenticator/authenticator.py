from abc import ABC, abstractmethod

class IAuthenticator(ABC):

  @abstractmethod
  def decode_token(token: str):
    pass

  @abstractmethod
  def generate_token(payload: str):
    pass