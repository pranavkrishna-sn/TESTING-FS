from typing import Optional
from backend.models.user import User

class UserRepository:

    def __init__(self, db):
        self.db = db

    def add_user(self, user: User) -> User:
        query = """
        INSERT INTO users (email, password, first_name, last_name, phone_number, address, login_attempts, is_locked, created_at, updated_at)
        VALUES (:email, :password, :first_name, :last_name, :phone_number, :address, :login_attempts, :is_locked, :created_at, :updated_at)
        RETURNING id;
        """
        cursor = self.db.cursor()
        cursor.execute(query, user.dict())
        user.id = cursor.fetchone()[0]
        self.db.commit()
        return user

    def get_user_by_email(self, email: str) -> Optional[User]:
        query = "SELECT * FROM users WHERE email = :email;"
        cursor = self.db.cursor()
        cursor.execute(query, {"email": email})
        row = cursor.fetchone()
        if row:
            return User(id=row[0], email=row[1], password=row[2], first_name=row[3], last_name=row[4], phone_number=row[5], address=row[6], login_attempts=row[7], is_locked=row[8], created_at=row[9], updated_at=row[10])
        return None

    def update_user(self, user: User) -> None:
        query = """
        UPDATE users SET email = :email, password = :password, first_name = :first_name, last_name = :last_name, phone_number = :phone_number, address = :address, login_attempts = :login_attempts, is_locked = :is_locked, updated_at = :updated_at
        WHERE id = :id;
        """
        cursor = self.db.cursor()
        cursor.execute(query, user.dict())
        self.db.commit()