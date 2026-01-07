from dataclasses import dataclass
from datetime import datetime


@dataclass
class Session:
    id: int
    user_id: int
    token: str
    expires_at: datetime
    last_activity_at: datetime
    created_at: datetime