import os
import pytest
import httpx
import time
from dotenv import load_dotenv

load_dotenv(dotenv_path=f".env.{os.getenv('NODE_ENV', 'test')}")

async def test_should_create_and_get_user():
  async with httpx.AsyncClient() as client:
    headers = {
      "Authorization": f"Bearer {os.getenv('JWT_TOKEN')}"
    }
    input_data = {
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
    create_response = await client.post(
      f"{os.getenv('APPLICATION_URL')}/questions/discursive-questions",
      headers=headers,
      json=input_data
    )
    assert create_response.status_code == 201 or create_response.status_code == 200
    data = create_response.json()
    id_question = data["id"]
    get_response = await client.get(
      f"{os.getenv('APPLICATION_URL')}/questions/discursive-questions/{id_question}",
      headers=headers
    )
    assert get_response.status_code == 200
    question = get_response.json()
    assert question["id_author"] == input_data["id_author"]
    assert question["title"] == input_data["title"]
    assert question["prompt"] == input_data["prompt"]
    assert question["expected_answer"] == input_data["expected_answer"]
    assert question["criteria"] == input_data["criteria"]
    assert question["tags"] == input_data["tags"]
    assert question["topic"] == input_data["topic"]
    assert question["difficulty"] == input_data["difficulty"]
    assert question["grade_level"] == input_data["grade_level"]
