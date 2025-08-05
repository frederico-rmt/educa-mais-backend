import os
import time
from dotenv import load_dotenv
from src.application.controller.discursive_answer_controller import DiscursiveAnswerController
from src.application.repository.discursive_answer_sql_database import DiscursiveAnswerSqlDatabase
from src.infra.ai.google_genai_driver import GoogleGenAIDriver
from src.infra.ai.question_ai_feedback_gateway import QuestionAIFeedbackGateway
from src.application.controller.discursive_question_controller import DiscursiveQuestionController
from src.application.repository.discursive_question_sql_database import DiscursiveQuestionSqlDatabase
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
discursive_question_repository = DiscursiveQuestionSqlDatabase(pgDriver)
discursive_answer_repository = DiscursiveAnswerSqlDatabase(pgDriver)

google_genai_driver = GoogleGenAIDriver(os.getenv("GEMINI_API_KEY"), os.getenv("GEMINI_MODEL"))
question_ai_gateway = QuestionAIFeedbackGateway(google_genai_driver)

UserController(http, user_repository, bCryptDriver, authenticator)
DiscursiveQuestionController(http, discursive_question_repository)
DiscursiveAnswerController(http, discursive_answer_repository, discursive_question_repository, question_ai_gateway)

app = http.app

async def startup_event():
  print('-'.center(50, '-'))
  print(f"Server online at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}".center(50))
  print('Educa Mais built by Frederico Machado'.center(50))
  print('-'.center(50, '-'))