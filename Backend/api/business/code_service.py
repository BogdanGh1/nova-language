from api.domain.code import Code
from api.infrastructure.code_repository import CodeRepository

class CodeService:
    def __init__(self, code_repository: CodeRepository) -> None:
        self.code_repository = code_repository
    
    def get_codes(self,user_id, game_name):
        return self.code_repository.find_all_by_user_id_and_game_name(user_id,game_name)
    
    def save_new_code(self, user_id: int, game_name: str, code: str):
        return self.code_repository.add_new_code(user_id,game_name,code)

    def update_code(self, user_id: int, game_name: str, code_id, new_code: str):
        return self.code_repository.update_code(user_id,game_name, code_id, new_code)
