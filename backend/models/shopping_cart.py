from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class ShoppingCart(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    session_id: Optional[str] = None
    product_id: int
    quantity: int
    added_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True
        validate_assignment = True