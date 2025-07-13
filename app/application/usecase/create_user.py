from dataclasses import dataclass
from app.application.repository.user_repository import IUserRepository
from app.domain.entities.user import User
from app.domain.value_objects.email import Email
from app.domain.value_objects.raw_password import RawPassword
from app.infra.hasher.hasher import IHasher

@dataclass
class CreateUserInput:
    email: str
    password: str

class CreateUser():
  def __init__(self, user_repository: IUserRepository, hasher: IHasher):
    self._user_repository = user_repository
    self._hasher = hasher

  async def execute(self, input: CreateUserInput):
    raw_password = RawPassword(input.password)
    hashed_password = self._hasher.encrypt(raw_password.value)
    email = Email(input.email)
    user = User(email, hashed_password)
    await self._user_repository.create_user(user)