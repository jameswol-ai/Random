from dataclasses import dataclass, field
import uuid
import random

@dataclass
class Design:
    id: str
    type: str
    domain: str
    bedrooms: int
    rooms: list
    area_sqm: int
    structure: dict
    cost: int
    fitness: dict = field(default_factory=dict)
    score: int = 0


def new_id():
    return str(uuid.uuid4())[:8].upper()