import datetime
from src.domain.entities.user import User
from src.application.repository.user_repository import IUserRepository
from src.infra.authenticator.authenticator import IAuthenticator
from src.infra.hasher.hasher import IHasher

class Login:
  def __init__(self, user_repository: IUserRepository, hasher: IHasher, authenticator: IAuthenticator):
    self._user_repository = user_repository
    self._hasher = hasher
    self._authenticator = authenticator

  async def execute(self, email: str, password: str):
    try:
      user = await self._get_valid_user(email, password)
      return self._generate_auth_payload(user)
    except ValueError as e:
      raise AuthenticationError("Invalid email or password") from e

  async def _get_valid_user(self, email: str, password: str) -> User:
    user = await self._user_repository.get_user(email)
    if not user or not self._hasher.decrypt(password, user.password):
      raise AuthenticationError("Invalid email or password")
    return user

  def _generate_auth_payload(self, user: User) -> dict:
    user_payload = {
      "email": user.email.value,
      "name": user.name,
      "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=6),
    }
    token = self._authenticator.generate_token(user_payload)
    return {
      "access_token": token,
      "token_type": 'bearer',
      "user": user_payload
    }

class AuthenticationError(Exception):
    pass