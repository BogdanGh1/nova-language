from api.domain.entity import Entity


class Code(Entity):
    def __init__(self, id, code: str, game_name: str, user_id: int) -> None:
        super().__init__(id)
        self.code = code
        self.game_name = game_name
        self.user_id = user_id
