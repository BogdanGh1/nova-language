from fastapi import APIRouter, Depends
from pydantic import BaseModel
from api.business.user_service import UserService
from api.infrastructure.user_repository import UserRepository

router = APIRouter(prefix="/users")

user_service = None


@router.on_event("startup")
async def startup_event():
    global user_service
    user_repository = UserRepository()
    user_service = UserService(user_repository)

def get_user_service():
    return  user_service

class UserData(BaseModel):
    username: str
    password: str

@router.post("/")
async def register(user_data: UserData, user_service: UserService = Depends(get_user_service)):
    try:
        user_service.register(user_data.username, user_data.password)
        return True
    except Exception as e:
        raise e

@router.post("/login")
async def login(user_data: UserData, user_service: UserService = Depends(get_user_service)):
    valid = user_service.login(user_data.username, user_data.password)
    return valid