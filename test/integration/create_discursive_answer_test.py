import os
from dotenv import load_dotenv
import pytest
from src.infra.ai.google_genai_driver import GoogleGenAIDriver
from src.infra.ai.question_ai_feedback_gateway import QuestionAIFeedbackGateway
from src.domain.value_objects.uuid_identifier import UuidIdentifier
from src.infra.database.pg_driver import PgDriver
from src.application.repository.discursive_answer_sql_database import DiscursiveAnswerSqlDatabase
from src.application.repository.discursive_question_sql_database import DiscursiveQuestionSqlDatabase
from src.application.usecase.create_discursive_answer import CreateDiscursiveAnswer
from src.application.usecase.get_discursive_answer import GetDiscursiveAnswer
from src.application.usecase.create_discursive_question import CreateDiscursiveQuestion

@pytest.fixture
def load_test_env():
  load_dotenv(dotenv_path=".env.test", override=True)
  return {
    "host": os.getenv("PG_HOST"),
    "port": int(os.getenv("PG_PORT")),
    "database": os.getenv("PG_DB"),
    "user": os.getenv("PG_USER"),
    "password": os.getenv("PG_PASSWORD"),
    "gemini_api_key": os.getenv("GEMINI_API_KEY"),
    "gemini_model": os.getenv("GEMINI_MODEL")
  }

@pytest.fixture
def setup_question_data():
  return {
    "id_author": "b372c8fc-67fd-4565-aed2-2a159d2fd80d",
    "title": "A causa da Primeira Guerra Mundial",
    "prompt": "Explique as principais causas que levaram ao início da Primeira Guerra Mundial.",
    "expected_answer": "As principais causas incluem o assassinato do arquiduque Franz Ferdinand, alianças militares, nacionalismo e imperialismo.",
    "criteria": "Mencionar pelo menos três causas com explicações históricas.",
    "tags": ["história", "guerra"],
    "topic": "história",
    "difficulty": "médio",
    "grade_level": 9
  }

@pytest.fixture
def setup_answer_data():
  return {
    "id_student": "ea8996d0-7968-4126-8a24-7970e2142b82",
    "answer": "A Primeira Guerra Mundial começou por conta de alianças políticas, nacionalismo e assassinato do arquiduque.",
  }

@pytest.fixture()
async def create_answer_usecase(load_test_env):
  driver = PgDriver(
    load_test_env["host"],
    load_test_env["port"],
    load_test_env["database"],
    load_test_env["user"],
    load_test_env["password"]
  )
  question_repo = DiscursiveQuestionSqlDatabase(driver)
  answer_repo = DiscursiveAnswerSqlDatabase(driver)
  ai_driver = GoogleGenAIDriver(load_test_env["gemini_api_key"], load_test_env["gemini_model"])
  ai_gateway = QuestionAIFeedbackGateway(ai_driver)
  create_answer = CreateDiscursiveAnswer(question_repo, answer_repo, ai_gateway)
  create_question = CreateDiscursiveQuestion(question_repo)
  get_answer = GetDiscursiveAnswer(answer_repo)
  yield {
    "create_answer": create_answer,
    "get_answer": get_answer,
    "create_question": create_question
  }
  await driver.close()

@pytest.mark.asyncio
async def test_create_discursive_answer(create_answer_usecase, setup_question_data, setup_answer_data):
  create_question = create_answer_usecase["create_question"]
  id_question = await create_question.execute(**setup_question_data)

  id_student = setup_answer_data["id_student"]
  student_answer = setup_answer_data["answer"]
  create_answer = create_answer_usecase["create_answer"]
  get_answer = create_answer_usecase["get_answer"]

  result = await create_answer.execute(uuid_question=id_question, uuid_student=id_student, student_answer=student_answer)
  assert "id_answer" in result
  assert isinstance(result["grade"], int)
  assert isinstance(result["feedback"], str)

  answer = await get_answer.execute(result["id_answer"])

  assert isinstance(answer.id, UuidIdentifier)
  assert answer.id_question.value == id_question
  assert answer.id_student.value == id_student
  assert answer.answer == student_answer
  assert isinstance(answer.grade, int)
  assert answer.grade >= 0 and answer.grade <= 100
  assert isinstance(answer.feedback, str)
  assert answer.created_at is not None
  assert answer.corrected_at is not None
