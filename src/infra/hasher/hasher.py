from abc import ABC, abstractmethod

class IHasher():
  @abstractmethod
  def encrypt(self, text: str) -> str:
    pass

  def decrypt(self, text: str, hashed_text: str) -> str:
    pass