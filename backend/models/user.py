from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: int
    email: str
    password_hash: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime