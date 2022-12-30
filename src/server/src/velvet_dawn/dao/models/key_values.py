import enum

from velvet_dawn.dao import db


class Keys(str, enum.Enum):
    MAP_WIDTH = 'MAP_WIDTH'
    MAP_HEIGHT = 'MAP_HEIGHT'

    PHASE = 'PHASE'  # 0 = lobby, 1 = setup, 2 = in game
    TURN = 'TURN'  # Turn number - only increments once each player has taken a turn
    TURN_START = 'TURN_START'
    ACTIVE_TURN = 'ACTIVE_TURN'  # The current team or player who's turn it is

    MODE = 'MODE'  # Teams or all v all.



class KeyValues(db.Model):
    __tablename__ = 'key_values'

    key = db.Column(db.Enum(Keys), primary_key=True)
    value = db.Column(db.Text)
