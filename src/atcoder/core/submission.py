import dataclasses
import datetime
import enum
import typing


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
class Submission:
    id: int
    status: typing.Optional[SubmissionStatus] = None
    submission_datetime: typing.Optional[datetime.datetime] = None
    task_id: typing.Optional[str] = None
    user: typing.Optional[str] = None
    language: typing.Optional[str] = None
    score: typing.Optional[int] = None
    code_size_kb: typing.Optional[int] = None
    exec_time_ms: typing.Optional[int] = None  # ms
    memory_usage_kb: typing.Optional[int] = None  # kB
    contest_id: typing.Optional[str] = None
    language_id: typing.Optional[int] = None  # 4047 for PyPy3
    code: typing.Optional[str] = None
    judge_details: typing.Optional[typing.List[JudgeResult]] = None
