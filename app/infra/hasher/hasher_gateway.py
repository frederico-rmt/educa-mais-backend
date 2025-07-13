from app.infra.hasher.hasher import IHasher

class HasherGateway(IHasher):
  def __init__(self, hasher: IHasher):
    self._hasher = hasher

  def encrypt(self, text: str):
    hashed = self._hasher.encrypt(text)
    return hashed

  def decrypt(self, text, hashed_text):
    return self._hasher.decrypt(text, hashed_text)