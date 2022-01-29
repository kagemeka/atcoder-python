import enum
import typing
import dataclasses
import datetime


class SubmissionStatus(enum.Enum):
    AC = enum.auto()
    WA = enum.auto()
    RE = enum.auto()
    TLE = enum.auto()
    MLE = enum.auto()
    QLE = enum.auto()
    CE = enum.auto()
    OLE = enum.auto()
    IE = enum.auto()
    WJ = enum.auto()
    WR = enum.auto()
    JUDGING = enum.auto()


def status_from_str(status: str) -> typing.Optional[SubmissionStatus]:
    return SubmissionStatus.__members__.get(status.upper())


@dataclasses.dataclass
class JudgeResult:
    case_name: str
    status: SubmissionStatus
    exec_time: int
    memory_usage: int


@dataclasses.dataclass
class SubmissionSummary:
    datetime: datetime.datetime
    task_id: str
    user: str
    language: str
    score: int
    code_size: int
    status: SubmissionStatus
    exec_time: int  # ms
    memory_usage: int  # kB
    code: typing.Optional[str] = None
    judge_details: typing.Optional[JudgeResult] = None


@dataclasses.dataclass
class Submission:
    id: int
    contest_id: str
    summary: typing.Optional[SubmissionSummary] = None
    code: typing.Optional[str] = None
    judge_details: typing.Optional[typing.List[JudgeResult]] = None
