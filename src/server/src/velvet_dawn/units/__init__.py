from typing import List, Optional

from velvet_dawn.dao import db
from velvet_dawn.dao.models import UnitInstance
from . import movement, upgrades


# TODO Test this


def get_unit(unit_id: str):
    return db.session.query(UnitInstance).where(UnitInstance.entity_id == unit_id).one_or_none()


def get_unit_by_id(unit_id: int) -> Optional[UnitInstance]:
    return db.session.query(UnitInstance).where(UnitInstance.id == unit_id).one_or_none()


def get_unit_at_position(x: int, y: int) -> Optional[UnitInstance]:
    return db.session.query(UnitInstance).where(UnitInstance.x == x, UnitInstance.y == y).one_or_none()


def list(player: str = None, commander_only=False) -> List[UnitInstance]:
    query = db.session.query(UnitInstance)

    if player:
        query = query.where(UnitInstance.player == player)

    if commander_only:
        query = query.where(UnitInstance.commander == True)

    return query.all()
