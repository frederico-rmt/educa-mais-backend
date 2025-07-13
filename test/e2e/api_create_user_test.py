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
    timestamp = int(time.time() * 1000)
    input_data = {
      "password": "Coxinha123",
      "email": f"john.doe{timestamp}@example.com"
    }
    create_response = await client.post(
      f"{os.getenv('APPLICATION_URL')}/users",
      json=input_data,
      headers=headers
    )
    assert create_response.status_code == 201 or create_response.status_code == 200
    get_response = await client.get(
      f"{os.getenv('APPLICATION_URL')}/users/{input_data['email']}",
      headers=headers
    )
    assert get_response.status_code == 200
    user = get_response.json()
    assert user["password"] == input_data["password"]
    assert user["email"]["value"] == input_data["email"]