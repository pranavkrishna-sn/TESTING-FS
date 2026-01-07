from dataclasses import dataclass
from datetime import datetime


@dataclass
class ShoppingCart:
    id: int
    user_id: int | None
    session_id: str | None
    total_price: float
    created_at: datetime
    updated_at: datetime