import typing

import requests

from atcoder.core.auth import InvalidSessionError, is_logged_in
from atcoder.core.crawl.submit import (
    SubmitPostParams,
    get_submit_page,
    post_submission,
)
from atcoder.core.language import Language
from atcoder.core.scrape.submit import scrape_csrf_token, scrape_languages


async def submit_task(
    session: requests.Session,
    contest_id: str,
    task_id: str,
    source_code: str,
    language_id: int,
) -> None:
    if not is_logged_in(session):
        raise InvalidSessionError
    response = await get_submit_page(session, contest_id)
    token = await scrape_csrf_token(response.content)
    params = SubmitPostParams(
        task_id=task_id,
        language_id=language_id,
        source_code=source_code,
        csrf_token=token,
    )
    await post_submission(session, contest_id, params)


async def fetch_languages(
    session: requests.Session,
) -> typing.List[Language]:
    if not is_logged_in(session):
        raise InvalidSessionError
    response = await get_submit_page(session, "abc001")
    return await scrape_languages(response.content)
