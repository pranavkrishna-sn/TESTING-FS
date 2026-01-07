from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: int
    email: str
    password_hash: str
    failed_login_attempts: int
    is_locked: bool
    last_login_at: datetime | None
    created_at: datetime
    updated_at: datetime