import typing

import bs4

from atcoder.core.scrape.contest import scrape_contest
from atcoder.core.scrape.utils import parse_html
from atcoder.core.task import Task


async def scrape_tasks(html: bytes) -> typing.List[Task]:
    contest = await scrape_contest(html)

    async def scrape_task(row: bs4.element.Tag) -> Task:
        infos = row.find_all("td")
        return Task(
            id=infos[1].a.get("href").split("/")[-1],
            name=infos[1].text,
            order=infos[0].text,
            time_limit_ms=int(float(infos[2].text.split()[0]) * 1000),
            memory_limit_kb=int(infos[3].text.split()[0]) * 1000,
            contest_id=contest.id,
        )

    soup = await parse_html(html)
    return [await scrape_task(row) for row in soup.table.tbody.find_all("tr")]
