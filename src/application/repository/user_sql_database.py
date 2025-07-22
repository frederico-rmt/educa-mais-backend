from src.domain.value_objects.uuid_identifier import UuidIdentifier
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
    query = f'INSERT INTO "{self._schema}"."{self._table}" (uuid, name, email, password, role) VALUES (%s, %s, %s, %s, %s)'
    await self._driver.query(query, [user.id.value, user.name, user.email.value, user.password, user.role])

  async def get_user(self, email: str) -> User:
    query = f'SELECT uuid, name, email, password, role FROM "{self._schema}"."{self._table}" WHERE email = %s'
    row = await self._driver.query(query, [email])
    if not row:
      raise ValueError("User not found")
    user_data = row[0]
    uuid = user_data[0]
    id = UuidIdentifier(uuid)
    name = user_data[1]
    email_vo = Email(user_data[2])
    password = user_data[3]
    role = user_data[4]
    user = User(id, name, email_vo, password, role)
    return user