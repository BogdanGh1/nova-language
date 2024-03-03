class Action:
    def __init__(self, action_type: str) -> None:
        self.type = action_type

    def __str__(self) -> str:
        return self.type

    def __repr__(self) -> str:
        return str(self)

    def to_dict(self) -> dict:
        return {"type": self.type}


class PrintAction(Action):
    def __init__(self, action_type: str, text: str) -> None:
        super().__init__(action_type)
        self.text = text

    def __str__(self) -> str:
        return super().__str__() + " " + self.text

    def __repr__(self) -> str:
        return str(self)

    def to_dict(self) -> dict:
        dict = super().to_dict()
        dict["text"] = self.text
        return dict
