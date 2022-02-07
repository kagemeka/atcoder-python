import dataclasses
import typing


@dataclasses.dataclass
class Language:
    id: int
    name: str
    version: str
    category: typing.Optional[str] = None
    file_extensions: typing.Optional[typing.List[str]] = None


_NAME_TO_EXTENSION = {
    "C++": ".cpp",
}
