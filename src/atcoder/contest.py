import asyncio
import typing

from atcoder.core.contest import Contest
from atcoder.core.crawl.contests import get_contests_page
from atcoder.core.crawl.contests_archive import get_contests_archive_page
from atcoder.core.scrape.contests import (
    scrape_permanent_contests,
    scrape_running_contests,
    scrape_upcoming_contests,
)
from atcoder.core.scrape.contests_archive import scrape_finished_contests


async def fetch_all_contests() -> typing.AsyncIterator[typing.List[Contest]]:
    response = await get_contests_page()
    contests = await scrape_upcoming_contests(response.content)
    if contests is not None:
        yield contests
    yield await scrape_permanent_contests(response.content)
    contests = await scrape_running_contests(response.content)
    if contests is not None:
        yield contests
    page = 1
    while True:
        response = await get_contests_archive_page(page)
        contests = await scrape_finished_contests(response.content)
        if contests is None:
            return
        yield contests
        page += 1
        await asyncio.sleep(0.2)


async def fetch_contest_details() -> None:
    ...


async def register() -> None:
    ...
