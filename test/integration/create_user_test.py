from dotenv import load_dotenv
import os
import pytest
import time
from src.infra.database.pg_driver import PgDriver
from src.application.repository.user_sql_database import UserSqlDatabase
from src.application.usecase.create_user import CreateUser
from src.application.usecase.create_user import CreateUserInput
from src.infra.hasher.bcrypt_driver import BCryptDriver
from src.application.usecase.get_user import GetUser
from src.infra.hasher.hasher_gateway import HasherGateway

@pytest.fixture
def load_test_env():
  load_dotenv(dotenv_path=".env.test", override=True)
  return {
    "host": os.getenv("PG_HOST"),
    "port": int(os.getenv("PG_PORT")),
    "database": os.getenv("PG_DB"),
    "user": os.getenv("PG_USER"),
    "password": os.getenv("PG_PASSWORD"),
  }

@pytest.fixture
def setup_user_data():
  return {
    "email": f"john.{time.time()}@mail.com",
    "password": "Coxinha123",
    "name": f"John {time.time()}",
    "role": "teacher"
  }

@pytest.fixture()
async def create_user_usecase(load_test_env):
  database_driver = PgDriver(
    load_test_env["host"],
    load_test_env["port"],
    load_test_env["database"],
    load_test_env["user"],
    load_test_env["password"])
  user_repository = UserSqlDatabase(database_driver)
  hasher = BCryptDriver(12)
  hasher_gateway = HasherGateway(hasher)
  create_user = CreateUser(user_repository, hasher_gateway)
  get_user = GetUser(user_repository)
  yield {
    "create_user": create_user,
    "get_user": get_user,
    "hasher": hasher_gateway
  }
  await database_driver.close()

async def test_create_user(setup_user_data, create_user_usecase):
  email = setup_user_data["email"]
  password = setup_user_data["password"]
  name = setup_user_data["name"]
  role = setup_user_data["role"]
  create_user = create_user_usecase["create_user"]
  get_user = create_user_usecase["get_user"]
  await create_user.execute(name, email, password, role)
  user = await get_user.execute(email)
  assert user.email.value == email
  assert user.name == name
  assert user.role == role
  hasher = create_user_usecase["hasher"]
  assert hasher.decrypt(password, user.password) == True