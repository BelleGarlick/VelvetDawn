from typing import List, Optional

from velvet_dawn.dao import db
from velvet_dawn.dao.models import UnitInstance
from . import movement


# TODO Test this


def get_unit(unit_id: str):
    return db.session.query(UnitInstance).where(UnitInstance.entity_id == unit_id).one_or_none()


def get_unit_by_id(unit_id: int) -> Optional[UnitInstance]:
    return db.session.query(UnitInstance).where(UnitInstance.id == unit_id).one_or_none()


def get_unit_at_position(x: int, y: int):
    return db.session.query(UnitInstance).where(UnitInstance.x == x, UnitInstance.y == y).one_or_none()


def list(player: str = None) -> List[UnitInstance]:
    if player:
        return db.session.query(UnitInstance).where(UnitInstance.player == player).all()
    return db.session.query(UnitInstance).all()
