from app.application.repository.user_repository import IUserRepository

class GetUser():
  def __init__(self, user_repository: IUserRepository):
    self._user_repository = user_repository

  async def execute(self, email: str):
    user = await self._user_repository.get_user(email)
    return user