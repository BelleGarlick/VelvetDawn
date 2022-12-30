import dataclasses
from typing import Optional, List


@dataclasses.dataclass
class Coordinate:
    x: int
    y: int

    def __hash__(self):
        return self.x * 10000 + self.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
