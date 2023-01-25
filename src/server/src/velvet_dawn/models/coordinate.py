import dataclasses
from typing import Union


@dataclasses.dataclass
class Coordinate:
    x: Union[int, float]
    y: Union[int, float]

    def __hash__(self):
        return self.x * 10000 + self.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
