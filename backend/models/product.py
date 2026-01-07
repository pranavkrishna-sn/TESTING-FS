from dataclasses import dataclass
from datetime import datetime


@dataclass
class Product:
    id: int
    name: str
    description: str
    price: float
    stock_quantity: int
    created_at: datetime
    updated_at: datetime