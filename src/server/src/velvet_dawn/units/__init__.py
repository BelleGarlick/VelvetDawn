from typing import List, Optional

from velvet_dawn.dao import db
from velvet_dawn.dao.models import Entity
from . import movement


# TODO Test this


def get_unit(unit_id: str):
    return db.session.query(Entity).where(Entity.entity_id == unit_id).one_or_none()


def get_unit_by_id(unit_id: int) -> Optional[Entity]:
    return db.session.query(Entity).where(Entity.id == unit_id).one_or_none()


def get_unit_at_position(x: int, y: int):
    return db.session.query(Entity).where(Entity.pos_x == x, Entity.pos_y == y).one_or_none()


def list(player: str = None) -> List[Entity]:
    if player:
        return db.session.query(Entity).where(Entity.player == player).all()
    return db.session.query(Entity).all()
