# app/interfaces/database.py
from abc import ABC, abstractmethod
from typing import Any

class IDatabaseDriver(ABC):
    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def query(self, query: str, params: tuple = ()) -> Any:
        pass