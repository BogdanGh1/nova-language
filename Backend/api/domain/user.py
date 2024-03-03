from api.domain.entity import Entity


class User(Entity):
    def __init__(self, id, username, password) -> None:
        super.__init__(id)
        self.username = username
        self.password = password
