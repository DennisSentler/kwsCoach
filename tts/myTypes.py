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
    REPLICATION = 3
    TIME_SHIFT = 4

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
    
    def __str__(self):
        return f"{self.text} - {self.languages}"

@dataclass
class Augmentation:
    type: AugmentationType
    parameter: list[int]

    def __eq__(self, other):
        if isinstance(other, Augmentation):
            return self.type == other.type
        return False

    def __lt__(self, other):
        return self.type < other.type

    def __str__(self):
        return f"{self.type.name} {self.parameter}"

    