import enum


class Phase(str, enum.Enum):
    Lobby = "lobby"
    Setup = "setup"
    GAME = "game"
    GAME_OVER = "over"
