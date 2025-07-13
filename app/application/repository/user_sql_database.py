from app.application.repository.user_repository import IUserRepository
from app.infra.database import database_driver
from app.domain.entities.user import User
from app.domain.value_objects.email import Email

class UserSqlDatabase(IUserRepository):
  def __init__(self, driver: database_driver):
    self._driver = driver
    self._table = 'user'
    self._schema = 'educa_mais'

  async def create_user(self, user: User):
    query = f'INSERT INTO "{self._schema}"."{self._table}" (email, password) VALUES (%s, %s)'
    await self._driver.query(query, [user.email.value, user.password])

  async def get_user(self, email: str) -> User:
    query = f'SELECT email, password FROM "{self._schema}"."{self._table}" WHERE email = %s'
    row = await self._driver.query(query, [email])
    if not row:
      raise ValueError("User not found")
    user_data = row[0]
    email_vo = Email(user_data[0])
    password = user_data[1]
    user = User(email_vo, password)
    return user