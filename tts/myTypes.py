from dataclasses import dataclass
from enum import Enum

class Provider(Enum):
    GOOGLE = 0
    WATSON = 1
    AZURE = 3

class Gender(Enum):
    MALE = 0
    FEMALE = 1

@dataclass
class Voice:
    provider: Provider
    name: str
    language: str
    gender: Gender

    def __str__(self):
        return f"{self.provider}_{self.name}_{self.language}_{self.gender}"