from abc import ABC, abstractmethod
from typing import Any
from src.domain.entities.user import User

class IUserRepository(ABC):

    @abstractmethod
    def create_user(self, user: User) -> None:
        pass

    @abstractmethod
    def get_user(self, email: str) -> User:
        pass