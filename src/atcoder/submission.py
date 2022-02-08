import asyncio
import dataclasses
import datetime
import enum
import logging
import typing

import aiohttp
import bs4
import pandas as pd
import requests

import atcoder.auth
import atcoder.contest
import atcoder.language
import atcoder.utils

_LOGGER = logging.getLogger(__name__)
REQUEST_CHUNK_SIZE = 10
REQUEST_INTERVAL_SEC = 0


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


def _status_from_str(status: str) -> typing.Optional[SubmissionStatus]:
    return SubmissionStatus.__members__.get(status.upper())


def _status_to_string(status: SubmissionStatus) -> str:
    if status == SubmissionStatus.JUDGING:
        return "Judging"
    else:
        return status.name


class LanguageParseError(Exception):
    pass


def _parse_language(language_text: str) -> atcoder.language.Language:
    language = atcoder.language._language_from_text(language_text)
    if language is not None:
        return language
    (
        language_name,
        compiler_or_runtime,
        *_,
    ) = atcoder.language._parse_language_text(language_text)
    language = atcoder.language._language_from_name(language_name)
    if language is not None:
        return language
    if compiler_or_runtime is None:
        raise LanguageParseError
    return atcoder.utils._unwrap(
        atcoder.language._language_from_compiler(compiler_or_runtime),
    )


@dataclasses.dataclass(frozen=True)
class JudgeResult:
    case_name: str
    status: SubmissionStatus
    exec_time_ms: int
    memory_usage_kb: int


@dataclasses.dataclass(frozen=True)
class Summary:
    datetime: datetime.datetime
    task_id: str
    username: str
    language: atcoder.language.Language
    score: int
    code_size_kb: int
    status: SubmissionStatus
    exec_time_ms: typing.Optional[int] = None
    memory_usage_kb: typing.Optional[int] = None


@dataclasses.dataclass(frozen=True)
class Details:
    code: str
    judge_results: typing.Optional[typing.List[JudgeResult]] = None


@dataclasses.dataclass
class SubmissionResult:
    id: int
    summary: Summary
    details: typing.Optional[Details] = None


async def _get_submission_page(
    session: aiohttp.ClientSession,
    contest_id: str,
    submission_id: int,
) -> aiohttp.ClientResponse:
    url = (
        f"{atcoder.contest._CONTESTS_URL}/{contest_id}"
        f"/submissions/{submission_id}"
    )
    _LOGGER.info(f"get {url}")
    return await session.get(url)


def _scrape_id(html: str) -> int:
    import re

    soup = atcoder.scrape._parse_html(html)
    match = re.match(r"^.*\#(\d+).*$", soup.find(class_="h2").text)
    return int(atcoder.utils._unwrap(match).group(1))


def _scrape_summary(html: str) -> Summary:
    import datetime

    soup = atcoder.scrape._parse_html(html)
    infos = soup.table.find_all("tr")
    assert len(infos) >= 7
    if soup.table.find(class_="waiting-judge") is not None:
        status = SubmissionStatus.WJ
    else:
        status = atcoder.utils._unwrap(
            _status_from_str(infos[6].td.text.split()[-1]),
        )
    if len(infos) == 9:
        exec_time_ms = atcoder.scrape._strip_unit(infos[7].td.text)
        memory_usage_kb = atcoder.scrape._strip_unit(infos[8].td.text)
    else:
        exec_time_ms = None
        memory_usage_kb = None
    return Summary(
        datetime=datetime.datetime.strptime(
            infos[0].time.text,
            "%Y-%m-%d %H:%M:%S%z",
        ),
        task_id=infos[1].a.get("href").split("/")[-1],
        username=infos[2].a.get("href").split("/")[-1],
        language=_parse_language(infos[3].td.text.strip()),
        score=int(infos[4].td.text),
        code_size_kb=atcoder.scrape._strip_unit(infos[5].td.text),
        status=status,
        exec_time_ms=exec_time_ms,
        memory_usage_kb=memory_usage_kb,
    )


def _scrape_code(html: str) -> str:
    soup = atcoder.scrape._parse_html(html)
    return typing.cast(str, soup.find(id="submission-code").text)


def _scrape_judge_results(
    html: str,
) -> typing.Optional[typing.List[JudgeResult]]:
    tables = pd.read_html(html)
    if len(tables) <= 3:  # no judge results.
        return None
    table = tables[-1]
    table.rename(
        columns={
            "Case Name": "case_name",
            "Status": "status",
            "Exec Time": "exec_time_ms",
            "Memory": "memory_usage_kb",
        },
        inplace=True,
    )
    table["exec_time_ms"] = table["exec_time_ms"].map(
        atcoder.scrape._strip_unit
    )
    table["memory_usage_kb"] = table["memory_usage_kb"].map(
        atcoder.scrape._strip_unit
    )
    table["status"] = table["status"].map(_status_from_str)
    records = table.to_dict(orient="records")
    return [JudgeResult(**record) for record in records]


def _scrape_details(html: str) -> Details:
    return Details(
        code=_scrape_code(html),
        judge_results=_scrape_judge_results(html),
    )


def _scrape_submission_result(html: str) -> SubmissionResult:
    return SubmissionResult(
        id=_scrape_id(html),
        summary=_scrape_summary(html),
        details=_scrape_details(html),
    )


@dataclasses.dataclass
class SubmissionsSearchParams:
    task_id: typing.Optional[str] = None
    language_category: typing.Optional[str] = None
    language_id: typing.Optional[int] = None
    status: typing.Optional[str] = None
    username: typing.Optional[str] = None


_TO_URL_PARAMS: typing.Final[typing.Dict[str, str]] = {
    "task_id": "f.Task",
    "language_category": "f.LanguageName",
    "language_id": "f.Language",
    "status": "f.Status",
    "username": "f.User",
}


def _to_url_param(param: str) -> typing.Optional[str]:
    return _TO_URL_PARAMS.get(param)


def _make_url_params(
    search_params: typing.Optional[SubmissionsSearchParams] = None,
    page: typing.Optional[int] = None,
) -> typing.Dict[str, typing.Union[str, int]]:
    url_params: typing.Dict[str, typing.Union[str, int]] = dict()
    if search_params is not None:
        for param, value in dataclasses.asdict(search_params).items():
            if value is None:
                continue
            url_params[atcoder.utils._unwrap(_to_url_param(param))] = value
    if page is not None:
        url_params["page"] = page
    return url_params


async def _get_submissions_page(
    session: aiohttp.ClientSession,
    contest_id: str,
    search_params: typing.Optional[SubmissionsSearchParams] = None,
    page: typing.Optional[int] = None,
) -> aiohttp.ClientResponse:
    url = f"{atcoder.contest._CONTESTS_URL}/{contest_id}/submissions"
    _LOGGER.info(f"get {url}, page: {page}")
    return await session.get(
        url,
        params=_make_url_params(search_params, page),
    )


def _get_my_submissions_page(
    session: requests.Session,
    contest_id: str,
    search_params: typing.Optional[SubmissionsSearchParams] = None,
    page_id: typing.Optional[int] = None,
) -> requests.Response:
    url = f"{atcoder.contest._CONTESTS_URL}/{contest_id}/submissions/me"
    _LOGGER.info(f"get {url}")
    return session.get(
        url=url,
        params=_make_url_params(search_params, page_id),
    )


def _scrape_task_ids(html: str) -> typing.List[str]:
    return atcoder.utils._unwrap(
        atcoder.scrape._scrape_html_options(html, "select-task")
    )


def _scrape_language_categories(html: str) -> typing.List[str]:
    return atcoder.utils._unwrap(
        atcoder.scrape._scrape_html_options(html, "select-language")
    )


def _scrape_submission_statuses(html: str) -> typing.List[str]:
    return atcoder.utils._unwrap(
        atcoder.scrape._scrape_html_options(html, "select-status")
    )


def _scrape_pagination(
    html: str,
) -> typing.Optional[typing.Tuple[int, int]]:
    soup = atcoder.scrape._parse_html(html)
    pagination = soup.find(class_="pagination")
    if pagination is None:
        return None
    pages = pagination.find_all("li")
    if not pages:
        _LOGGER.info("no submissions")
        return None
    _LOGGER.info(f"found {len(pages)} pages")
    current_page = int(pagination.find(class_="active").text)
    last_page = int(pages[-1].text)
    return current_page, last_page


def _scrape_submission_row(row: bs4.element.Tag) -> SubmissionResult:
    infos = row.find_all("td")
    assert len(infos) >= 8
    if row.find(class_="waiting-judge") is not None:
        status = SubmissionStatus.WJ
    else:
        status = atcoder.utils._unwrap(
            _status_from_str(infos[6].text.split()[-1])
        )
    if len(infos) == 10:
        exec_time_ms = atcoder.scrape._strip_unit(infos[7].text)
        memory_usage_kb = atcoder.scrape._strip_unit(infos[8].text)
    else:
        exec_time_ms = None
        memory_usage_kb = None
    summary = Summary(
        datetime=datetime.datetime.strptime(
            infos[0].time.text,
            "%Y-%m-%d %H:%M:%S%z",
        ),
        task_id=infos[1].a.get("href").split("/")[-1],
        username=infos[2].a.get("href").split("/")[-1],
        language=_parse_language(infos[3].text.strip()),
        score=int(infos[4].text),
        code_size_kb=atcoder.scrape._strip_unit(infos[5].text),
        status=status,
        exec_time_ms=exec_time_ms,
        memory_usage_kb=memory_usage_kb,
    )
    return SubmissionResult(
        id=infos[-1].a.get("href").split("/")[-1],
        summary=summary,
    )


def _scrape_submissions(
    html: str,
) -> typing.Iterator[SubmissionResult]:
    soup = atcoder.scrape._parse_html(html)
    table = soup.table
    if table is None:
        return
    for row in table.tbody.find_all("tr"):
        yield _scrape_submission_row(row)


async def _get_submissions_pages(
    session: aiohttp.ClientSession,
    contest_id: str,
    search_params: typing.Optional[SubmissionsSearchParams] = None,
) -> typing.AsyncIterator[aiohttp.ClientResponse]:
    response = await _get_submissions_page(
        session,
        contest_id,
        search_params,
        1,
    )
    pagination = _scrape_pagination(await response.text())
    if pagination is None:
        return
    _, last_page = pagination
    for i in range(1, last_page + 1, REQUEST_CHUNK_SIZE):
        get_pages = [
            asyncio.create_task(
                _get_submissions_page(session, contest_id, search_params, page)
            )
            for page in range(i, min(i + REQUEST_CHUNK_SIZE, last_page + 1))
        ]
        await asyncio.sleep(REQUEST_INTERVAL_SEC)
        for get_page in get_pages:
            yield await get_page


def _get_my_submissions_pages(
    session: requests.Session,
    contest_id: str,
    search_params: typing.Optional[SubmissionsSearchParams] = None,
) -> typing.Iterator[requests.Response]:
    response = _get_my_submissions_page(session, contest_id, search_params, 1)
    pagination = _scrape_pagination(response.text)
    if pagination is None:
        return
    _, last_page = pagination
    for page in range(1, last_page + 1):
        yield _get_my_submissions_page(
            session,
            contest_id,
            search_params,
            page,
        )


async def _fetch_submission_results(
    session: aiohttp.ClientSession,
    contest_id: str,
    params: typing.Optional[SubmissionsSearchParams] = None,
    page: typing.Optional[int] = None,
) -> typing.AsyncIterator[SubmissionResult]:
    response = await _get_submissions_page(session, contest_id, params, page)
    _LOGGER.info(f"fetch: submissions for {contest_id} page: {page}.")
    for submission in _scrape_submissions(await response.text()):
        yield submission


async def fetch_all_submission_results(
    session: aiohttp.ClientSession,
    contest_id: str,
    params: typing.Optional[SubmissionsSearchParams] = None,
) -> typing.AsyncIterator[SubmissionResult]:
    async for response in _get_submissions_pages(session, contest_id, params):
        for submission in _scrape_submissions(await response.text()):
            yield submission


def _fetch_my_submission_results(
    session: requests.Session,
    contest_id: str,
    params: typing.Optional[SubmissionsSearchParams] = None,
    page: typing.Optional[int] = None,
) -> typing.Iterator[SubmissionResult]:
    if not atcoder.auth._is_logged_in(session):
        raise atcoder.auth.InvalidSessionError
    response = _get_my_submissions_page(session, contest_id, params, page)
    _LOGGER.info(f"fetch: submissions for {contest_id}.")
    for submission in _scrape_submissions(response.text):
        yield submission


def fetch_all_my_submission_results(
    session: requests.Session,
    contest_id: str,
    params: typing.Optional[SubmissionsSearchParams] = None,
) -> typing.Iterator[SubmissionResult]:
    for response in _get_my_submissions_pages(session, contest_id, params):
        for submission in _scrape_submissions(response.text):
            yield submission


async def fetch_submission_details(
    session: aiohttp.ClientSession,
    contest_id: str,
    submission_id: int,
) -> SubmissionResult:
    response = await _get_submission_page(session, contest_id, submission_id)
    return _scrape_submission_result(await response.text())


async def _fetch_submission_results_page_count(
    session: aiohttp.ClientSession,
    contest_id: str,
    params: typing.Optional[SubmissionsSearchParams] = None,
) -> int:
    response = await _get_submissions_page(session, contest_id, params)
    pagination = _scrape_pagination(await response.text())
    if pagination is None:
        return 0
    _, last_page = pagination
    return last_page


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
