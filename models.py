from pydantic import BaseModel
from typing import List

class UserStoryInput(BaseModel):
    functionality: str
    system: str
    base_story: str

class UserStoryOutput(BaseModel):
    persona: str
    need: str
    reason: str
    acceptance_criteria: List[str]
