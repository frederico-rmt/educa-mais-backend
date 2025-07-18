from dataclasses import dataclass
from src.application.repository.user_repository import IUserRepository
from src.domain.entities.user import User
from src.domain.value_objects.email import Email
from src.domain.value_objects.raw_password import RawPassword
from src.infra.hasher.hasher import IHasher

@dataclass
class CreateUserInput:
    email: str
    password: str

class CreateUser():
  def __init__(self, user_repository: IUserRepository, hasher: IHasher):
    self._user_repository = user_repository
    self._hasher = hasher

  async def execute(self, name: str, email: str, password: str):
    raw_password = RawPassword(password)
    hashed_password = self._hasher.encrypt(raw_password.value)
    email = Email(email)
    user = User(name, email, hashed_password)
    await self._user_repository.create_user(user)