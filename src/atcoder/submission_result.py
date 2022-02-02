import asyncio
import logging
import typing

import requests

from atcoder.core.auth import InvalidSessionError, is_logged_in
from atcoder.core.crawl.submission_result import get_submission_page
from atcoder.core.crawl.submission_results import (
    SubmissionsSearchParams,
    get_my_submissions_page,
    get_submissions_page,
)
from atcoder.core.scrape.submission_result import scrape_submission_result
from atcoder.core.scrape.submission_results import (
    scrape_pagination,
    scrape_submissions,
)
from atcoder.core.submission_result import SubmissionResult

logger = logging.getLogger(__name__)


async def fetch_submission_results(
    contest_id: str,
    params: typing.Optional[SubmissionsSearchParams] = None,
    page: typing.Optional[int] = None,
) -> typing.Optional[typing.List[SubmissionResult]]:
    response = await get_submissions_page(contest_id, params, page)
    submissions = await scrape_submissions(response.content)
    logger.info(f"fetch: submissions for {contest_id}.")
    return submissions


async def fetch_all_submission_results(
    contest_id: str,
    params: typing.Optional[SubmissionsSearchParams] = None,
) -> typing.AsyncIterator[typing.List[SubmissionResult]]:
    page = 1
    while True:
        submissions = await fetch_submission_results(contest_id, params, page)
        if submissions is None:
            return
        yield submissions
        page += 1
        await asyncio.sleep(0.2)


async def fetch_my_submission_results(
    session: requests.Session,
    contest_id: str,
    params: typing.Optional[SubmissionsSearchParams] = None,
    page: typing.Optional[int] = None,
) -> typing.Optional[typing.List[SubmissionResult]]:
    if not is_logged_in:
        raise InvalidSessionError
    response = await get_my_submissions_page(session, contest_id, params, page)
    submissions = await scrape_submissions(response.content)
    logger.info(f"fetch: submissions for {contest_id}.")
    return submissions


async def fetch_all_my_submission_results(
    session: requests.Session,
    contest_id: str,
    params: typing.Optional[SubmissionsSearchParams] = None,
) -> typing.AsyncIterator[typing.List[SubmissionResult]]:
    page = 1
    while True:
        submissions = await fetch_my_submission_results(
            session,
            contest_id,
            params,
            page,
        )
        if submissions is None:
            return
        yield submissions
        page += 1
        await asyncio.sleep(0.2)


async def fetch_submission_details(
    contest_id: str,
    submission_id: int,
) -> SubmissionResult:
    response = await get_submission_page(contest_id, submission_id)
    return await scrape_submission_result(response.content)


async def fetch_submission_results_page_count(
    contest_id: str,
    params: typing.Optional[SubmissionsSearchParams] = None,
) -> int:
    response = await get_submissions_page(contest_id, params)
    pagination = await scrape_pagination(response.content)
    if pagination is None:
        return 0
    _, last_page = pagination
    return last_page
