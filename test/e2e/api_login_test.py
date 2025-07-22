import os
import httpx
import time
from dotenv import load_dotenv

load_dotenv(dotenv_path=f".env.{os.getenv('NODE_ENV', 'test')}")

async def test_validate_login():
  async with httpx.AsyncClient() as client:
    create_headers = {
      "Authorization": f"Bearer {os.getenv('JWT_TOKEN')}"
    }
    timestamp = int(time.time() * 1000)
    user_data = {
      "password": "Coxinha123",
      "email": f"john.doe{timestamp}@example.com",
      "name": f"John {timestamp}",
      "role": "teacher"
    }
    create_response = await client.post(
      f"{os.getenv('APPLICATION_URL')}/users",
      json=user_data,
      headers=create_headers
    )
    assert create_response.status_code == 201 or create_response.status_code == 200
    input_login = {
      "email": user_data["email"],
      "password": user_data["password"]
    }
    login_headers = {
      "Content-Type": "application/json",
      "Accept": "application/json"
    }
    login_response = await client.post(
      f"{os.getenv('APPLICATION_URL')}/users/login",
      headers=login_headers,
      json=input_login
    )
    assert login_response.status_code == 200
    decoded = login_response.json()
    assert decoded["token_type"] == 'bearer'
    assert decoded["user"]["email"] == user_data["email"]
    assert decoded["user"]["name"] == user_data["name"]