import dataclasses
import datetime
import typing

from atcoder.submission_status import SubmissionStatus


@dataclasses.dataclass
class SubmissionInfo:
    submission_time: datetime.datetime
    task: str
    user: str
    language: int
    score: int
    code_size: int
    status: SubmissionStatus
    exec_time: int  # ms
    memory: int  # kB
