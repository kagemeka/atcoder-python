import dataclasses


@dataclasses.dataclass
class Language:
    language: str
    version: str
    id: int
    language_name: str
