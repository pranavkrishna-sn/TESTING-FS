from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class Category(BaseModel):
    id: Optional[int] = None
    name: str
    parent_id: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True
        validate_assignment = True