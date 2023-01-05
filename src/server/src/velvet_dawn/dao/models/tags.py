import enum

from velvet_dawn.dao import db
from velvet_dawn.dao.models.tile import TileInstance
from velvet_dawn.dao.models.entities import UnitInstance


class TagParent(str, enum.Enum):
    Unit = 'unit'
    Tile = 'tile'
    World = 'world'


class Tag(db.Model):
    __tablename__ = 'tags'

    pk = db.Column(db.Integer, primary_key=True)

    # Store the instance ids, world doesn't need one since there is only one instance
    unit_instance_id = db.Column(db.Integer, db.ForeignKey(UnitInstance.id))
    tile_instance_id = db.Column(db.Integer, db.ForeignKey(TileInstance.id))
    parent_type = db.Column(db.Enum(TagParent), nullable=False)

    tag = db.Column(db.String, nullable=False)

    db.UniqueConstraint(unit_instance_id, tile_instance_id, tag, parent_type)


def __get_base_query(instance_id: int, parent_type: TagParent):
    base_query = db.session.query(Tag).where(
        Tag.parent_type == parent_type
    )

    if parent_type == TagParent.Unit:
        base_query = base_query.where(Tag.unit_instance_id == instance_id)
    if parent_type == TagParent.Tile:
        base_query = base_query.where(Tag.tile_instance_id == instance_id)

    return base_query


def create_tag_obj(instance_id: int, parent_type: TagParent, tag: str):
    tag_obj = Tag(parent_type=parent_type, tag=tag)

    if parent_type == TagParent.Unit:
        tag_obj.unit_instance_id = instance_id
    if parent_type == TagParent.Tile:
        tag_obj.tile_instance_id = instance_id

    return tag_obj


def add_tag(instance_id: int, parent_type: TagParent, tag: str, commit=True):
    """ Add a tag to given the parent type and id """
    if not tag.startswith("tag:"):
        tag = f"tag:{tag}"

    remove_tag(instance_id, parent_type, tag, commit=False)
    db.session.merge(create_tag_obj(instance_id, parent_type, tag))

    if commit:
        db.session.commit()


def remove_tag(instance_id: int, parent_type: TagParent, tag: str, commit=True):
    """ Remove a tag given the parent type and id """
    if not tag.startswith("tag:"):
        tag = f"tag:{tag}"

    __get_base_query(instance_id, parent_type).where(Tag.tag == tag).delete()

    if commit:
        db.session.commit()


def list_tags(instance_id: int, parent_type: TagParent):
    """ List all tags for the given type and id """
    return [x.tag for x in __get_base_query(instance_id, parent_type).all()]


def has_tag(instance_id: int, parent_type: TagParent, tag: str):
    """ Check if the item type exists """
    item = __get_base_query(instance_id, parent_type).where(Tag.tag == tag).one_or_none()
    return bool(item)
