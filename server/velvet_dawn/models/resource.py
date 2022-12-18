import dataclasses
import enum
from pathlib import Path


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
