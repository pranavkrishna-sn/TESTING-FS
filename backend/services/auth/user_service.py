from backend.repositories.auth.user_repository import UserRepository
from backend.models.user import User
import bcrypt

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register_user(self, email: str, password: str) -> User:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user = User(email=email, password=hashed_password)
        return self.user_repository.add_user(new_user)

    def validate_user(self, email: str, password: str) -> bool:
        user = self.user_repository.get_user_by_email(email)
        if not user:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))