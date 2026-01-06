from typing import Optional
from backend.models.session import Session

class SessionRepository:

    def __init__(self, db):
        self.db = db

    def create_session(self, session: Session) -> Session:
        query = """
        INSERT INTO sessions (user_id, created_at, expires_at)
        VALUES (:user_id, :created_at, :expires_at)
        RETURNING id;
        """
        cursor = self.db.cursor()
        cursor.execute(query, session.dict())
        session.id = cursor.fetchone()[0]
        self.db.commit()
        return session

    def get_session_by_user_id(self, user_id: int) -> Optional[Session]:
        query = "SELECT * FROM sessions WHERE user_id = :user_id;"
        cursor = self.db.cursor()
        cursor.execute(query, {"user_id": user_id})
        row = cursor.fetchone()
        if row:
            return Session(id=row[0], user_id=row[1], created_at=row[2], expires_at=row[3])
        return None