from abc import ABC, abstractmethod

class IHttpServer(ABC):
  @abstractmethod
  def listen_port(self, port: int):
    pass

  def register(self, method: str, endpoint: str, callback: function):
    pass