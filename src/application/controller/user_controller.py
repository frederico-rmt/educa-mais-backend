from src.application.repository.user_repository import IUserRepository
from src.infra.authenticator.authenticator import IAuthenticator
from src.infra.hasher.hasher import IHasher
from src.application.usecase.login import Login
from src.application.usecase.create_user import CreateUser
from src.application.usecase.get_user import GetUser

class UserController:
  def __init__(self, http_server, user_database: IUserRepository, hasher_gateway: IHasher, authenticator: IAuthenticator):
    self._user_database = user_database
    self._hasher_gateway = hasher_gateway
    self._authenticator = authenticator

    http_server.register('post', '/users/login', self._make_login(), False)
    http_server.register('post', '/users', self._create_user(), False)
    http_server.register('get', '/users/{email}', self._get_user())

  def _make_login(self):
    async def handler(headers, query, params, body):
      email = body['email']
      password = body['password']
      login = Login(self._user_database, self._hasher_gateway, self._authenticator)
      result = await login.execute(email, password)
      return result
    return handler

  def _create_user(self):
    async def handler(headers, query, params, body):
      email = body['email']
      password = body['password']
      name = body['name']
      role = body['role']
      create_user = CreateUser(self._user_database, self._hasher_gateway)
      await create_user.execute(name, email, password, role)
      return {'message': 'account-created'}
    return handler

  def _get_user(self):
    async def handler(headers, query, params, body):
      email = params['email']
      get_user = GetUser(self._user_database)
      user = await get_user.execute(email)
      user_dto = {
        "email": user.email.value,
        "name": user.name
      }
      return user_dto
    return handler