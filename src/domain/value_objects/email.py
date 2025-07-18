# app/domain/value_objects/email.py
from dataclasses import dataclass
import re

class Email:
    def __init__(self, value: str):
        if not self._is_valid(value):
            raise ValueError(f"Email inválido: {value}")
        self.value = value
        self.value = value.lower()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value: str):
        if not self._is_valid(new_value):
            raise ValueError(f"Email inválido: {new_value}")
        self._value = new_value

    def _is_valid(self, email: str) -> bool:
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        return re.match(pattern, email) is not None

    def __eq__(self, other):
        if isinstance(other, Email):
            return self.value.lower() == other.value.lower()
        return False

    def __str__(self):
        return self.value