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


def status_to_string(status: SubmissionStatus) -> str:
    if status == SubmissionStatus.JUDGING:
        return "Judging"
    else:
        return status.name


@dataclasses.dataclass(frozen=True)
class JudgeResult:
    case_name: str
    status: SubmissionStatus
    exec_time_ms: int
    memory_usage_kb: int


@dataclasses.dataclass(frozen=True)
class SubmissionSummary:
    datetime: datetime.datetime
    task_id: str
    username: str
    language_string: str
    score: int
    code_size_kb: int
    status: SubmissionStatus
    exec_time_ms: typing.Optional[int] = None
    memory_usage_kb: typing.Optional[int] = None


@dataclasses.dataclass(frozen=True)
class SubmissionDetails:
    code: str
    judge_results: typing.Optional[typing.List[JudgeResult]] = None


@dataclasses.dataclass
class SubmissionResult:
    id: int
    summary: SubmissionSummary
    details: typing.Optional[SubmissionDetails] = None
