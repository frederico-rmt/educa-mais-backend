import os
import time
from dotenv import load_dotenv
from src.application.controller.user_controller import UserController
from src.application.repository.user_sql_database import UserSqlDatabase
from src.infra.database.pg_driver import PgDriver
from src.infra.http.fastapi_driver import FastAPIAdapter
from src.infra.hasher.bcrypt_driver import BCryptDriver

load_dotenv(dotenv_path=".env.dev", override=True)

http = FastAPIAdapter()

pgDriver = PgDriver(
  os.getenv("PG_HOST"),
  int(os.getenv("PG_PORT")),
  os.getenv("PG_DB"),
  os.getenv("PG_USER"),
  os.getenv("PG_PASSWORD")
)
bCryptDriver = BCryptDriver(int(os.getenv("BCRYPT_SALTS")))
user_repository = UserSqlDatabase(pgDriver)

UserController(http, user_repository, bCryptDriver)

app = http.app

@app.on_event("startup")
async def startup_event():
  print('-'.center(50, '-'))
  print('Server online at 2025-07-17 23:10:00'.center(50))
  print('Educa Mais built by Frederico Machado'.center(50))
  print('-'.center(50, '-'))