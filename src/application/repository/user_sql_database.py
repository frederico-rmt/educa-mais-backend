from src.application.repository.user_repository import IUserRepository
from src.infra.database import database_driver
from src.domain.entities.user import User
from src.domain.value_objects.email import Email

class UserSqlDatabase(IUserRepository):
  def __init__(self, driver: database_driver):
    self._driver = driver
    self._table = 'users'
    self._schema = 'educa_mais'

  async def create_user(self, user: User):
    query = f'INSERT INTO "{self._schema}"."{self._table}" (name, email, password) VALUES (%s, %s, %s)'
    await self._driver.query(query, [user.name, user.email.value, user.password])

  async def get_user(self, email: str) -> User:
    query = f'SELECT name, email, password FROM "{self._schema}"."{self._table}" WHERE email = %s'
    row = await self._driver.query(query, [email])
    if not row:
      raise ValueError("User not found")
    user_data = row[0]
    name = user_data[0]
    email_vo = Email(user_data[1])
    password = user_data[2]
    user = User(name, email_vo, password)
    return user