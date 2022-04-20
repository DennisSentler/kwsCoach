from dataclasses import dataclass
from enum import Enum
from enum import IntEnum

from typing import Dict

class Provider(Enum):
    GOOGLE = "GOOGLE"
    WATSON = "WATSON"
    AZURE = "AZURE"

class Gender(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"

class AugmentationType(IntEnum):
    TRIM_SILENCE = 1
    NORMALIZE_DURATION = 2
    REPLICATION_FACTOR = 3
    TIME_SHIFT = 4
    PITCH = 5
    TIME_STRETCH = 6
    VOLUME = 7
    GAUSSIAN_NOISE = 8
    BACKGROUND_NOISE = 9
    SHORT_NOISE = 10

@dataclass
class Voice:
    provider: Provider
    name: str
    language: str
    gender: Gender

    def __str__(self):
        return f"{self.provider.name}_{self.name}_{self.language}_{self.gender}"

@dataclass
class Word:
    text: str
    languages: list[str]
    is_random: bool = False
    quantity: int = 1
    
    def __str__(self):
        return f"{self.text} - {self.languages}"