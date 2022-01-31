import typing

from atcoder.core.contest import Contest, ContestStatus
from atcoder.core.scrape.contests import _scrape_contest
from atcoder.core.scrape.utils import parse_html


async def scrape_finished_contests(
    html: bytes,
) -> typing.Optional[typing.List[Contest]]:
    soup = await parse_html(html)
    if soup.table is None:
        return None
    contests = []

    for row in soup.table.tbody.find_all("tr"):
        contest = await _scrape_contest(row)
        contest.status = ContestStatus.FINISHED
        contests.append(contest)
    return contests


async def scrape_pagination(html: bytes) -> typing.Tuple[int, int]:
    soup = await parse_html(html)
    pagination = soup.find(class_="pagination")
    current = int(pagination.find(class_="active").text)
    last = int(pagination.find_all("li")[-1].text)
    return current, last
