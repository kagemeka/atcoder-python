import dataclasses
import typing


@dataclasses.dataclass
class Task:
    id: str
    name: typing.Optional[str] = None
    order: typing.Optional[str] = None  # A, B, ..., 001, 002, ...
    contest_id: typing.Optional[str] = None
    time_limit: typing.Optional[int] = None
    memory_limit: typing.Optional[int] = None
