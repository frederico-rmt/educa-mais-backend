import json
import os
import time
from dotenv import load_dotenv
import pytest
from src.application.repository.user_sql_database import UserSqlDatabase
from src.application.usecase.create_user import CreateUser
from src.application.usecase.login import AuthenticationError, Login
from src.infra.authenticator.authenticator_gateway import AuthenticatorGateway
from src.infra.authenticator.jwt_driver import JWTDriver
from src.infra.database.pg_driver import PgDriver
from src.infra.hasher.bcrypt_driver import BCryptDriver
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
    "secret_key": os.getenv("JWT_SECRET_KEY")
  }

@pytest.fixture
def setup_user_data():
  return {
    "email": f"john.{time.time()}@mail.com",
    "password": "Coxinha123",
    "name": f"John {time.time()}"
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
  authenticator = JWTDriver(os.getenv("PRIVATE_JWK"), os.getenv("PUBLIC_JWK"))
  authenticator_gateway = AuthenticatorGateway(authenticator)
  create_user = CreateUser(user_repository, hasher_gateway)
  login = Login(user_repository, hasher, authenticator_gateway)
  yield {
    "create_user": create_user,
    "login": login,
    "authenticator_gateway": authenticator_gateway
  }
  await database_driver.close()

async def test_validate_login(create_user_usecase, setup_user_data):
  email = setup_user_data["email"]
  password = setup_user_data["password"]
  name = setup_user_data["name"]
  create_user = create_user_usecase["create_user"]
  await create_user.execute(name, email, password)
  login = create_user_usecase["login"]
  login_response = await login.execute(email, password)
  authenticator_gateway = create_user_usecase["authenticator_gateway"]
  assert login_response["token_type"] == 'bearer'
  assert login_response["user"]["email"] == email
  assert login_response["user"]["name"] == name
  decoded_token = authenticator_gateway.decode_token(login_response["access_token"])
  assert decoded_token["email"] == email
  assert decoded_token["name"] == name

async def test_login_with_invalid_password_should_fail(create_user_usecase, setup_user_data):
  email = setup_user_data["email"]
  password = setup_user_data["password"]
  name = setup_user_data["name"]
  create_user = create_user_usecase["create_user"]
  await create_user.execute(name, email, password)
  login = create_user_usecase["login"]
  with pytest.raises(AuthenticationError) as exc_info:
    await login.execute(email, 'wrong_password')
  assert str(exc_info.value) == "Invalid email or password"

async def test_login_with_invalid_user(create_user_usecase):
  login = create_user_usecase["login"]
  with pytest.raises(AuthenticationError) as exc_info:
    await login.execute('not-existent@email.com', 'wrong_password')
  assert str(exc_info.value) == "Invalid email or password"