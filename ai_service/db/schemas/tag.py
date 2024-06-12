from typing import List
from pydantic import BaseModel

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int

    class Config:
        orm_mode = True

class TagUpdate(BaseModel):
    task_id: int
    tags: List[str]
