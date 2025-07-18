from src.application.usecase.create_user import CreateUser
from src.application.usecase.get_user import GetUser

class UserController:
  def __init__(self, http_server, user_database, hasher_gateway):
    self._user_database = user_database
    self._hasher_gateway = hasher_gateway

    # http_server.register('post', '/user/login', self._make_login())
    http_server.register('post', '/users', self._create_user())
    http_server.register('get', '/users/{email}', self._get_user())

  # def _make_login(self):
  #   async def handler(headers, query, params, body):
  #     input_data = {
  #       'email': body['email'],
  #       'password': body['password']
  #     }
  #     login = Login(self._user_database, self._hasher_gateway)
  #     result = await login.execute(input_data)
  #     return {'message': 'login-allowed' if result else 'login-disallowed'}
  #   return handler

  def _create_user(self):
    async def handler(headers, query, params, body):
      email = body['email']
      password = body['password']
      name = body['name']
      create_user = CreateUser(self._user_database, self._hasher_gateway)
      await create_user.execute(name, email, password)
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