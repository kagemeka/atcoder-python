import dataclasses
import logging
import typing

import bs4
import requests

import atcoder.auth
import atcoder.contest
import atcoder.language
import atcoder.scrape
import atcoder.utils

_LOGGER = logging.getLogger(__name__)


def _make_submit_url(contest_id: str) -> str:
    return f"{atcoder.contest._CONTESTS_URL}/{contest_id}/submit"


def _get_submit_page(
    session: requests.Session,
    contest_id: str,
) -> requests.models.Response:
    url = _make_submit_url(contest_id)
    _LOGGER.info(f"get {url}")
    return session.get(url)


@dataclasses.dataclass(frozen=True)
class SubmitPostParams:
    task_id: str
    language_id: int
    source_code: str
    csrf_token: str


def _scrape_csrf_token(html: str) -> str:
    soup = atcoder.scrape._parse_html(html)
    return atcoder.utils._unwrap(
        atcoder.scrape._scrape_csrf_token_in_form(soup.find_all("form")[1])
    )


def _post_submission(
    session: requests.Session,
    contest_id: str,
    post_params: SubmitPostParams,
) -> requests.models.Response:
    return session.post(
        url=_make_submit_url(contest_id),
        data={
            "data.TaskScreenName": post_params.task_id,
            "data.LanguageId": post_params.language_id,
            "sourceCode": post_params.source_code,
            "csrf_token": post_params.csrf_token,
        },
    )


def _scrape_task_ids(html: str) -> typing.List[str]:
    return atcoder.utils._unwrap(
        atcoder.scrape._scrape_html_options(html, "select-task")
    )


def _parse_language(section: bs4.Tag) -> atcoder.language.Language:
    language_text = section.text.strip()
    (
        name,
        compiler_or_runtime,
        version,
        compile_to,
    ) = atcoder.language._parse_language_text(language_text)
    return atcoder.language.Language(
        id=int(section.get("value")),
        text=language_text,
        name=name,
        compiler_or_runtime=compiler_or_runtime,
        version=version,
        compile_to=compile_to,
    )


def _scrape_languages(
    html: str,
) -> typing.List[atcoder.language.Language]:
    soup = atcoder.scrape._parse_html(html)
    form = soup.find_all("form")[1]
    section = form.find(id="select-lang").div
    languages = []
    for option in section.find_all("option")[1:]:
        languages.append(_parse_language(option))
    return languages


def submit_task(
    session: requests.Session,
    contest_id: str,
    task_id: str,
    source_code: str,
    language_id: int,
) -> None:
    if not atcoder.auth._is_logged_in(session):
        raise atcoder.auth.InvalidSessionError
    response = _get_submit_page(session, contest_id)
    token = _scrape_csrf_token(response.text)
    params = SubmitPostParams(
        task_id=task_id,
        language_id=language_id,
        source_code=source_code,
        csrf_token=token,
    )
    _post_submission(session, contest_id, params)


def fetch_languages(
    session: requests.Session,
) -> typing.List[atcoder.language.Language]:
    if not atcoder.auth._is_logged_in(session):
        raise atcoder.auth.InvalidSessionError
    response = _get_submit_page(session, "abc001")
    return _scrape_languages(response.text)
