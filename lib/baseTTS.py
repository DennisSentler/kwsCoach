from dataclasses import dataclass
from abc import ABC, abstractmethod
from enum import Enum

class TTSProvider(ABC):
    @abstractmethod
    def connect(self) -> bool:
        pass
    def getVoices(self) -> list:
        pass

class Gender(Enum):
    MALE = 0
    FEMALE = 1

@dataclass
class Voice:
    provider: str
    name: str
    language: str
    gender: Gender

    def __str__(self):
        return f"{self.provider} - {self.name} - {self.language} - {self.gender}"
