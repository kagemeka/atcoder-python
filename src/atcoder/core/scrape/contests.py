import datetime
import typing

import bs4

from atcoder.core.contest import Contest, ContestStatus
from atcoder.core.scrape.utils import parse_html


def parse_duration(duration: str) -> datetime.timedelta:
    hours, minutes = map(int, duration.split(":"))
    return datetime.timedelta(hours=hours, minutes=minutes)


async def _scrape_contest(row: bs4.element.Tag) -> Contest:
    infos = row.find_all("td")
    return Contest(
        id=infos[1].a.get("href").split("/")[-1],
        title=infos[1].a.text.strip(),
        start_datetime=datetime.datetime.strptime(
            infos[0].time.text,
            "%Y-%m-%d %H:%M:%S%z",
        ),
        duration=parse_duration(infos[2].text),
    )


async def scrape_running_contests(
    html: bytes,
) -> typing.Optional[typing.List[Contest]]:
    soup = await parse_html(html)
    section = soup.find(id="contest-table-action")
    if section is None:
        return None
    contests = []
    for row in section.table.tbody.find_all("tr"):
        contest = await _scrape_contest(row)
        contest.status = ContestStatus.RUNNING
        contests.append(contest)
    return contests


async def scrape_permanent_contests(html: bytes) -> typing.List[Contest]:
    soup = await parse_html(html)

    async def scrape_permanent_contest(row: bs4.element.Tag) -> Contest:
        infos = row.find_all("td")
        return Contest(
            id=infos[0].a.get("href").split("/")[-1],
            title=infos[0].a.text.strip(),
            status=ContestStatus.PERMANENT,
        )

    contests = []
    table = soup.find(id="contest-table-permanent").table
    for row in table.tbody.find_all("tr"):
        contest = await scrape_permanent_contest(row)
        contests.append(contest)
    return contests


async def scrape_upcoming_contests(
    html: bytes,
) -> typing.Optional[typing.List[Contest]]:
    soup = await parse_html(html)
    section = soup.find(id="contest-table-upcoming")
    if section is None:
        return None
    contests = []
    for row in section.table.tbody.find_all("tr"):
        contest = await _scrape_contest(row)
        contest.status = ContestStatus.UPCOMING
        contests.append(contest)
    return contests
