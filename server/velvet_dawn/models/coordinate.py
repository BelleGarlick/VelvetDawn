import dataclasses
from typing import Optional, List


@dataclasses.dataclass
class Coordinate:
    x: int
    y: int

    def __hash__(self):
        return self.x * 10000 + self.y
