import dataclasses


@dataclasses.dataclass
class Language:
    name: str
    version: str
    id: int
    category: str
