class Entities:
    def __init__(self, health):
        self.health = health

class Monsters(Entities):
    def __init__(self, health):
        super().__init__(health)

class Player(Entities):
    def __init__(self, health):
        super().__init__(health)