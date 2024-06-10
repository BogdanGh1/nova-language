from api.domain.code import Code
from api.infrastructure.code_repository import CodeRepository

class CodeService:
    def __init__(self, code_repository: CodeRepository) -> None:
        self.code_repository = code_repository
    