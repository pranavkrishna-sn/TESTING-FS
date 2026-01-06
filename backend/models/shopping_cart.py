from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator

class ShoppingCart(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    session_id: Optional[str] = None
    product_id: int
    quantity: int
    added_at: datetime = Field(default_factory=datetime.utcnow)

    @validator('quantity')
    def quantity_must_be_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError('Quantity must be a positive integer')
        return v

    class Config:
        orm_mode = True
        validate_assignment = True