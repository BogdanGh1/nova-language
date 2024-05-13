from api.domain.user import User
from api.infrastructure.user_repository import UserRepository

class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository
    
    def register(self, username:str, password: str) -> None:
        user = User(1,username,password)
        self.user_repository.add(user)

    def login(self, username: str, password: str) -> bool:
        user = self.user_repository.find_by_username_and_password(username, password)
        print (user)
        if user is not None:
            return True
        return False
    