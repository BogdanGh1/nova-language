from api.domain.entity import Entity


class Code(Entity):
    def __init__(self, id, text: str, username: str, game_name: str) -> None:
        super.__init__(id)
        self.text = text
        self.username = username
        self.game_name = game_name
