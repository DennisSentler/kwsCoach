from dataclasses import dataclass
from enum import Enum

class Provider(Enum):
    GOOGLE = "GOOGLE"
    WATSON = "WATSON"
    AZURE = "AZURE"

class Gender(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"

@dataclass
class Voice:
    provider: Provider
    name: str
    language: str
    gender: Gender

    def __str__(self):
        return f"{self.provider}_{self.name}_{self.language}_{self.gender}"

@dataclass
class Word:
    text: str
    languages: list[str]
    
    def __str__(self):
        return f"{self.text} - {self.languages}"