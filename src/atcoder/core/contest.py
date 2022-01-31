import dataclasses
import datetime
import enum
import typing


class ContestType(enum.Enum):
    BEGINNER = enum.auto()  # green, blue
    REGULAR = enum.auto()  # orange
    GRAND = enum.auto()  # red
    HEURISTIC = enum.auto()
    MISC = enum.auto()


class ContestColor(enum.Enum):
    GREEN = enum.auto()
    BLUE = enum.auto()
    ORANGE = enum.auto()
    RED = enum.auto()


@dataclasses.dataclass
class ContestStatus(enum.Enum):
    RUNNING = enum.auto()
    PERMANENT = enum.auto()
    UPCOMING = enum.auto()
    FINISHED = enum.auto()


@dataclasses.dataclass
class Contest:
    id: str
    title: str
    status: typing.Optional[ContestStatus] = None
    start_datetime: typing.Optional[datetime.datetime] = None
    duration: typing.Optional[datetime.timedelta] = None
    color: typing.Optional[ContestColor] = None
    type: typing.Optional[ContestType] = None
