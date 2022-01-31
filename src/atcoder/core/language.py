import dataclasses
import typing


@dataclasses.dataclass
class Language:
    id: int
    name: str
    version: str
    category: typing.Optional[str] = None
