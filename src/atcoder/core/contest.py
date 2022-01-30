import dataclasses
import datetime
import enum
import typing


class ContestType(enum.Enum):
    BEGINNER = enum.auto()  # green, blue
    REGULAR = enum.auto()  # orange
    GRAND = enum.auto()  # red
    HEURISTIC = enum.auto()
    UNRATED = enum.auto()


@dataclasses.dataclass
class ContestStatus(enum.Enum):
    RUNNING = enum.auto()
    PERMANENT = enum.auto()
    UPCOMING = enum.auto()
    FINISHED = enum.auto()


@dataclasses.dataclass
class Contest:
    id: str
    title: typing.Optional[str] = None
    type: typing.Optional[ContestType] = None
    status: typing.Optional[ContestStatus] = None
    start_datetime: typing.Optional[datetime.datetime] = None
    duration_sec: typing.Optional[int] = None
