from pydantic import BaseModel
from typing import Optional

class Pet(BaseModel):
    id: int
    name: str
    age: int
    type: str
    owner: Optional[str]