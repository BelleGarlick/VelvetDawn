import dataclasses
import enum
import json
from pathlib import Path
from typing import Dict


class ResourceType(str, enum.Enum):
    Image = 'image'
    Audio = 'audio'
    Font = 'font'


@dataclasses.dataclass
class Resource:
    id: str
    path: Path
    resource_type: ResourceType

    def json(self):
        return {
            "id": self.id,
            "type": self.resource_type
        }
