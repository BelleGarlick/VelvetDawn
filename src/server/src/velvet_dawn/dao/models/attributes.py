import enum
import time

from velvet_dawn.dao import db
from velvet_dawn.dao.models.tile import TileInstance
from velvet_dawn.dao.models.entities import UnitInstance
from velvet_dawn.logger import logger


class AttributeParent(str, enum.Enum):
    Unit = 'unit'
    Tile = 'tile'
    World = 'world'


class Attribute(db.Model):
    __tablename__ = 'attributes'

    pk = db.Column(db.Integer, primary_key=True)

    # Store the instance ids, world doesn't need one since there is only one instance
    unit_instance_id = db.Column(db.Integer, db.ForeignKey(UnitInstance.id))
    tile_instance_id = db.Column(db.Integer, db.ForeignKey(TileInstance.id))
    parent_type = db.Column(db.Enum(AttributeParent), nullable=False)

    key = db.Column(db.String, nullable=False)
    value = db.Column(db.String)
    type = db.Column(db.String, nullable=False)

    default_value = db.Column(db.String)
    default_type = db.Column(db.String, nullable=False)

    update_time = db.Column(db.Integer, nullable=False)

    db.UniqueConstraint(unit_instance_id, tile_instance_id, key, parent_type)

    def json(self):
        return {
            "instanceId": self.unit_instance_id or self.tile_instance_id,
            "parent": self.parent_type,
            "key": self.key,
            "value": _get_value(self)
        }


def _get_value(attribute: Attribute):
    """ This function returns the saved value in the form of the saved type """
    try:
        if attribute.type == "int": return int(attribute.value)
        elif attribute.type == "float": return float(attribute.value)
        elif attribute.type == "str": return str(attribute.value)
        elif attribute.type == "bool": return attribute.value == "True"
        elif attribute.type == "null": return None
        else:
            logger.error(f"Unknown attribute type: {attribute.type}")
    except Exception as e:
        logger.exception(e)

    return attribute.value


def _set_value(attribute: Attribute, value, set_default=False):
    """ Sets the value and type attribute """
    value_type = "null"
    if value is None: value_type = "null"
    elif isinstance(value, str): value_type = "str"
    elif isinstance(value, bool): value_type = "bool"
    elif isinstance(value, int): value_type = "int"
    elif isinstance(value, float): value_type = "float"
    else:
        logger.error(f"Invalid value type: {value}")

    if set_default:
        attribute.value = str(value)
        attribute.type = value_type
    else:
        attribute.default_value = str(value)
        attribute.default_type = value_type

    return attribute


def __get_query_attribute(instance_id, parent_type, key):
    """ Get the base attribute query """
    base_query = db.session.query(Attribute).where(
        Attribute.parent_type == parent_type,
        Attribute.key == key
    )

    if parent_type == AttributeParent.Unit:
        base_query = base_query.where(Attribute.unit_instance_id == instance_id)
    if parent_type == AttributeParent.Tile:
        base_query = base_query.where(Attribute.tile_instance_id == instance_id)

    return base_query


def get_attribute(instance_id, parent_type: AttributeParent, key: str, default=None):
    """ Get an attribute given the parent type, id and key """
    value = __get_query_attribute(instance_id, parent_type, key).one_or_none()

    if value:
        return _get_value(value)

    return default


def create_attribute_db_object(instance_id: int, parent_type: AttributeParent, key: str, value):
    """ Create the db object that will be added to the db """
    attr = Attribute(key=key, parent_type=parent_type, update_time=int(time.time()))

    if parent_type == AttributeParent.Unit:
        attr.unit_instance_id = instance_id
    if parent_type == AttributeParent.Tile:
        attr.tile_instance_id = instance_id

    _set_value(attr, value)
    _set_value(attr, value, set_default=True)

    return attr


def set_attribute(instance_id: int, parent_type: AttributeParent, key: str, value, commit=True):
    """ Set the value of an attribute """
    new_attribute = create_attribute_db_object(instance_id, parent_type, key, value)

    base_query = __get_query_attribute(instance_id, parent_type, key)

    # If item exists, then update, otherwise add
    item = base_query.one_or_none()
    if item:
        base_query.update({
            Attribute.value: new_attribute.value,
            Attribute.type: new_attribute.type,
            Attribute.update_time: int(time.time())
        })
    else:
        db.session.merge(new_attribute)

    if commit:
        db.session.commit()


def reset_attribute(instance_id: int, parent_type: AttributeParent, key: str, value_if_not_exists, commit=True):
    """ If the attribute exists, reset it to it's initial value """
    base_query = __get_query_attribute(instance_id, parent_type, key)

    # If item exists, then update, otherwise add
    item: Attribute = base_query.one_or_none()
    if item:
        base_query.update({
            Attribute.value: item.default_value,
            Attribute.type: item.default_type,
            Attribute.update_time: int(time.time())
        })

        if commit:
            db.session.commit()
    else:
        set_attribute(instance_id, parent_type, key, value_if_not_exists, commit=commit)
