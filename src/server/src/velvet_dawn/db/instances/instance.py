from abc import ABC


class Instance(ABC):

    @property
    def id(self):
        raise NotImplementedError

    @property
    def entity_id(self):
        raise NotImplementedError

    @property
    def player(self):
        return None

    def __hash__(self):
        raise NotImplementedError

    def __eq__(self, other):
        return hash(self) == hash(other)

    def set_attribute(self, key, value):
        raise NotImplementedError

    def get_attribute(self, key, default=None):
        raise NotImplementedError

    def reset_attribute(self, key, value_if_not_exists):
        raise NotImplementedError

    def add_tag(self, tag: str):
        raise NotImplementedError

    def remove_tag(self, tag: str):
        raise NotImplementedError

    def has_tag(self, tag: str):
        raise NotImplementedError
