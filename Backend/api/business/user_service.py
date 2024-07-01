from api.domain.user import User
from api.infrastructure.user_repository import UserRepository

import hashlib

def getHashedPassword(password: str) -> str:
    sha256_hash = hashlib.sha256()
    sha256_hash.update(password.encode())
    return sha256_hash.hexdigest()
class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository
    
    def register(self, username:str, password: str) -> None:
        # password = getHashedPassword(password)
        user = User(1,username,password)
        self.user_repository.add(user)

    def login(self, username: str, password: str) -> bool:
        # password = getHashedPassword(password)
        return self.user_repository.find_by_username_and_password(username, password)
    
    