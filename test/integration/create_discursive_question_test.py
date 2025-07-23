from dotenv import load_dotenv
import os
import pytest
import time
from src.domain.value_objects.uuid_identifier import UuidIdentifier
from src.infra.database.pg_driver import PgDriver
from src.application.repository.discursive_question_sql_database import DiscursiveQuestionSqlDatabase
from src.application.usecase.create_discursive_question import CreateDiscursiveQuestion
from src.application.usecase.get_discursive_question import GetDiscursiveQuestion

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
def setup_question_data():
  return {
    "id_author": 'b372c8fc-67fd-4565-aed2-2a159d2fd80d',
    "title": "A causa da Primeira Guerra Mundial",
    "prompt": "Explique as principais causas que levaram ao início da Primeira Guerra Mundial.",
    "expected_answer": "As principais causas incluem o assassinato do arquiduque Franz Ferdinand...",
    "criteria": "Responder ao menos três causas e explicar o contexto de cada uma.",
    "tags": ["world war", "europe"],
    "topic": "history",
    "difficulty": "medium",
    "grade_level": 9,
    "created_at": time.time()
  }

@pytest.fixture()
async def create_question_usecase(load_test_env):
  database_driver = PgDriver(
    load_test_env["host"],
    load_test_env["port"],
    load_test_env["database"],
    load_test_env["user"],
    load_test_env["password"])
  question_repository = DiscursiveQuestionSqlDatabase(database_driver)
  create_question = CreateDiscursiveQuestion(question_repository)
  get_question = GetDiscursiveQuestion(question_repository)
  yield {
    "create_question": create_question,
    "get_question": get_question
  }
  await database_driver.close()

async def test_create_question(setup_question_data, create_question_usecase):
  id_author = setup_question_data["id_author"]
  title = setup_question_data["title"]
  prompt = setup_question_data["prompt"]
  expected_answer = setup_question_data["expected_answer"]
  criteria = setup_question_data["criteria"]
  tags = setup_question_data["tags"]
  topic = setup_question_data["topic"]
  difficulty = setup_question_data["difficulty"]
  grade_level = setup_question_data["grade_level"]
  create_question = create_question_usecase["create_question"]
  get_question = create_question_usecase["get_question"]
  id_question = await create_question.execute(id_author, title, prompt, expected_answer, criteria, tags, topic, difficulty, grade_level)
  question = await get_question.execute(id_question)
  assert isinstance(question.id, UuidIdentifier)
  assert question.id_author.value == id_author
  assert question.title == title
  assert question.prompt == prompt
  assert question.expected_answer == expected_answer
  assert question.criteria == criteria
  assert question.tags == tags
  assert question.topic == topic
  assert question.difficulty == difficulty
  assert question.grade_level == grade_level
