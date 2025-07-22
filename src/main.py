import os
import time
from dotenv import load_dotenv
from src.infra.authenticator.jwt_driver import JWTDriver
from src.application.controller.user_controller import UserController
from src.application.repository.user_sql_database import UserSqlDatabase
from src.infra.database.pg_driver import PgDriver
from src.infra.http.fastapi_driver import FastAPIAdapter
from src.infra.hasher.bcrypt_driver import BCryptDriver

load_dotenv(dotenv_path=".env.dev", override=True)

authenticator = JWTDriver(os.getenv("PRIVATE_JWK"), os.getenv("PUBLIC_JWK"))
http = FastAPIAdapter(authenticator)

pgDriver = PgDriver(
  os.getenv("PG_HOST"),
  int(os.getenv("PG_PORT")),
  os.getenv("PG_DB"),
  os.getenv("PG_USER"),
  os.getenv("PG_PASSWORD")
)
bCryptDriver = BCryptDriver(int(os.getenv("BCRYPT_SALTS")))
user_repository = UserSqlDatabase(pgDriver)

UserController(http, user_repository, bCryptDriver, authenticator)

app = http.app

async def startup_event():
  print('-'.center(50, '-'))
  print(f"Server online at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}".center(50))
  print('Educa Mais built by Frederico Machado'.center(50))
  print('-'.center(50, '-'))