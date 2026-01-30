from .player import player


class figure:
    def __init__(self, player: player):
        self.player = player


class meeple(figure):
    def __init__(self, player: player):
        super().__init__(player)


class mayor(figure):
    def __init__(self, player: player):
        super().__init__(player)