class Action:
    def __init__(self, action_type: str) -> None:
        self.type = action_type


class PrintAction(Action):
    def __init__(self, action_type: str, text: str) -> None:
        super().__init__(action_type)
        self.text = text
