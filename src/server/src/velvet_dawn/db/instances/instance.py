from abc import ABC


class Instance(ABC):

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
