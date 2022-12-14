import enum


class Phase(str, enum.Enum):
    Lobby = "lobby"
    SETUP = "setup"
    GAME = "game"
    GAME_OVER = "over"
