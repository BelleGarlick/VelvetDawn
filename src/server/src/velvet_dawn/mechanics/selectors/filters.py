from typing import List, Optional

import velvet_dawn
from velvet_dawn import errors

from velvet_dawn.db.instances import Instance
from velvet_dawn.models.instances.instance import WorldInstance

""" Filtering module

This module contains the filters class which is applied to 
a selector. When the selector gets it's selection the filter
should be applied.
"""


class Filters:

    def __init__(self):
        # If any of these filters are none then don't apply
        self.allowed_ids = None
        self.allowed_tags = None
        self.min_range = None
        self.max_range = None
        self.exclude_self = False

    def add_filter(self, key: str, value: Optional[str] = None):
        """ Set a filter value """
        if key == "id":
            if self.allowed_ids is None:
                self.allowed_ids = set()
            self.allowed_ids.add(value)

        elif key == "exclude-self":
            self.exclude_self = True

        elif key == "tag":
            if not value.startswith("tag:"):
                value = f"tag:{value}"

            if self.allowed_tags is None:
                self.allowed_tags = set()
            self.allowed_tags.add(value)

        elif key == "range":
            velvet_dawn.validations.is_int(value, min=0, error_prefix=f"Range filter {value}")
            self.max_range = int(value)

        elif key == "min-range":
            velvet_dawn.validations.is_int(value, min=0, error_prefix=f"Min-range filter {value}")
            self.min_range = int(value)

        else:
            raise errors.ValidationError(f"Unknown filter: '{key}'.")

    def filter(
            self,
            instance: Instance,
            items: List[Instance]
    ) -> List[Instance]:
        """ Filter the list of given instances from the perspective of the
        given filter.

        Note, allowed tags are an 'and' clause but ids are an 'or' clause.
        """
        filtered_instances = []

        for item in items:
            valid = True

            # Check that the item has all tags
            if self.allowed_tags:
                for tag in self.allowed_tags:
                    valid = valid and item.has_tag(tag)

            # Check the id is in the list of given tags
            if self.allowed_ids:
                valid = valid and item.entity_id in self.allowed_ids

            # Check the max range if not world instance
            if self.max_range is not None and not isinstance(instance, WorldInstance):
                distance = velvet_dawn.map.get_distance(instance, item)
                valid = valid and distance <= self.max_range

            # Check the min range if not world instance
            if self.min_range is not None and not isinstance(instance, WorldInstance):
                distance = velvet_dawn.map.get_distance(instance, item)
                valid = valid and distance >= self.min_range

            if self.exclude_self:
                if instance.id == item.id and type(instance) == type(item):
                    valid = False

            if valid:
                filtered_instances.append(item)

        return filtered_instances
