import bcrypt
from app.infra.hasher.hasher import IHasher

class BCryptDriver(IHasher):
  def __init__(self, salts_number: int):
    self._salts_number = salts_number

  def encrypt(self, sent_password: str):
    raw_password = sent_password.encode('utf-8')
    hashed_password_bytes = bcrypt.hashpw(raw_password, bcrypt.gensalt(self._salts_number))
    hashed_password = hashed_password_bytes.decode('utf-8')
    return hashed_password

  def decrypt(self, sent_password: str, hashed_password: str):
    raw_password = sent_password.encode('utf-8')
    raw_hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(raw_password, raw_hashed_password)