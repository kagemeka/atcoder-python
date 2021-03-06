from __future__ import annotations

import dataclasses
import logging

import aiohttp
import bs4

import atcoder.contest
import atcoder.scrape

_LOGGER = logging.getLogger(__name__)


@dataclasses.dataclass
class Task:
    id: str
    name: str | None = None
    order: str | None = None  # A, B, ..., 001, 002, ...
    contest_id: str | None = None
    time_limit_ms: int | None = None
    memory_limit_kb: int | None = None


async def _get_task_page(
    session: aiohttp.ClientSession,
    contest_id: str,
    task_id: str,
) -> aiohttp.ClientResponse:
    url = f"{atcoder.contest._CONTESTS_URL}/{contest_id}/tasks/{task_id}"
    _LOGGER.info(f"get {url}")
    return await session.get(url)


async def _get_tasks_page(
    session: aiohttp.ClientSession,
    contest_id: str,
) -> aiohttp.ClientResponse:
    url = f"{atcoder.contest._CONTESTS_URL}/{contest_id}/tasks"
    _LOGGER.info(f"get {url}")
    return await session.get(url)


def _scrape_tasks(html: str) -> list[Task]:
    contest = atcoder.contest.scrape_contest(html)

    def scrape_row(row: bs4.element.Tag) -> Task:
        infos = row.find_all("td")
        return Task(
            id=infos[1].a.get("href").split("/")[-1],
            name=infos[1].text,
            order=infos[0].text,
            time_limit_ms=int(float(infos[2].text.split()[0]) * 1000),
            memory_limit_kb=int(infos[3].text.split()[0]) * 1000,
            contest_id=contest.id,
        )

    soup = atcoder.scrape._parse_html(html)
    return [scrape_row(row) for row in soup.table.tbody.find_all("tr")]
