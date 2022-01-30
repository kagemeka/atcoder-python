import dataclasses
import typing

import requests

from atcoder.core.crawl.constant import CONTESTS_URL
from atcoder.core.submission import SubmissionStatus
from atcoder.core.utils import unwrap


@dataclasses.dataclass
class RequestParams:
    task_id: typing.Optional[str] = None
    language_name: typing.Optional[str] = None
    language_id: typing.Optional[int] = None
    status: typing.Optional[SubmissionStatus] = None
    user: typing.Optional[str] = None


REQUEST_PARAMS: typing.Final[typing.Dict[str, str]] = {
    "task_id": "f.Task",
    "language_name": "f.LanguageName",
    "language_id": "f.Language",
    "status": "f.Status",
    "user": "f.User",
}


def to_url_param(param: str) -> typing.Optional[str]:
    return REQUEST_PARAMS.get(param)


def make_url_params(
    request_params: typing.Optional[RequestParams] = None,
    page_id: typing.Optional[int] = None,
) -> typing.Dict[str, typing.Union[str, int]]:
    url_params: typing.Dict[str, typing.Union[str, int]] = dict()
    if request_params is not None:
        for param, value in dataclasses.asdict(request_params).items():
            if value is None:
                continue
            param = unwrap(to_url_param(param))
            assert param is not None
            url_params[param] = value
    if page_id is not None:
        url_params["page"] = page_id
    return url_params


async def crawl_submissions_page(
    contest_id: str,
    request_params: typing.Optional[RequestParams] = None,
    page_id: typing.Optional[int] = None,
) -> requests.models.Response:
    url_params = make_url_params(request_params, page_id)
    url = f"{CONTESTS_URL}/{contest_id}/submissions"
    return requests.get(url, url_params)
