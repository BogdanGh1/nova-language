from fastapi import APIRouter, Depends
from pydantic import BaseModel
from api.business.code_service import CodeService
from api.infrastructure.code_repository import CodeRepository

router = APIRouter(prefix="/codes")

code_service = None

@router.on_event("startup")
async def startup_event():
    global code_service
    code_repository = CodeRepository()
    code_service = CodeService(code_repository)

def get_code_service():
    return  code_service

class CodeData(BaseModel):
    code:str

@router.post("/{user_id}/{game_name}")
async def save_new_code(user_id: int, game_name:str, code_data:CodeData, code_service: CodeService = Depends(get_code_service)):
    return code_service.save_new_code(user_id,game_name,code_data.code)[0]

@router.put("/{user_id}/{game_name}/{code_id}")
async def save_new_code(user_id: int, game_name:str, code_id:int, code_data:CodeData, code_service: CodeService = Depends(get_code_service)):
    return code_service.update_code(user_id, game_name, code_id, code_data.code)

@router.get("/{user_id}/{game_name}")
async def get_codes_for_user(user_id: int, game_name: str, code_service: CodeService = Depends(get_code_service)):
    return code_service.get_codes(user_id,game_name)
