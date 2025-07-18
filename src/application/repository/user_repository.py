# app/interfaces/database.py
from abc import ABC, abstractmethod
from typing import Any
from src.domain.entities.user import User

class IUserRepository(ABC):

    @abstractmethod
    def create_user(self) -> None:
        pass

    @abstractmethod
    def get_user(self) -> User:
        pass