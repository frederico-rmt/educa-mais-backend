import os
import pytest
import httpx
import time
from dotenv import load_dotenv

from src.domain.value_objects.uuid_identifier import UuidIdentifier

load_dotenv(dotenv_path=f".env.{os.getenv('NODE_ENV', 'test')}")

async def test_should_create_and_get_user():
  async with httpx.AsyncClient(timeout=60.0) as client:
    headers = {
      "Authorization": f"Bearer {os.getenv('JWT_TOKEN')}"
    }
    input_question = {
      "id_author": 'b372c8fc-67fd-4565-aed2-2a159d2fd80d',
      "title": "A causa da Primeira Guerra Mundial",
      "prompt": "Explique as principais causas que levaram ao início da Primeira Guerra Mundial.",
      "expected_answer": "As principais causas incluem o assassinato do arquiduque Franz Ferdinand...",
      "criteria": "Responder ao menos três causas e explicar o contexto de cada uma.",
      "tags": ["world war", "europe"],
      "topic": "history",
      "difficulty": "medium",
      "grade_level": 9
    }
    create_question_response = await client.post(
      f"{os.getenv('APPLICATION_URL')}/questions/discursive-questions",
      headers=headers,
      json=input_question
    )
    assert create_question_response.status_code == 201 or create_question_response.status_code == 200
    data = create_question_response.json()
    id_question = data["id"]
    input_answer = {
      "id_student": "ea8996d0-7968-4126-8a24-7970e2142b82",
      "id_question": id_question,
      "answer": "A Primeira Guerra Mundial começou por conta de alianças políticas, nacionalismo e assassinato do arquiduque."
    }
    create_answer_response = await client.post(
      f"{os.getenv('APPLICATION_URL')}/answers/discursive-answers",
      headers=headers,
      json=input_answer
    )
    assert create_answer_response.status_code == 201 or create_answer_response.status_code == 200
    data = create_answer_response.json()
    id_answer = data["id_answer"]
    get_answer_response = await client.get(
      f"{os.getenv('APPLICATION_URL')}/answers/discursive-answers/{id_answer}",
      headers=headers
    )
    assert get_answer_response.status_code == 200
    answer = get_answer_response.json()
    print(answer)
    UuidIdentifier(answer["id"])
    assert answer["id_question"] == id_question
    assert answer["id_student"] == input_answer["id_student"]
    assert answer["answer"] == input_answer["answer"]
    assert isinstance(answer["grade"], int)
    assert answer["grade"] >= 0 and answer["grade"] <= 100
    assert isinstance(answer["feedback"], str)
    assert answer["created_at"] is not None
    assert answer["corrected_at"] is not None
