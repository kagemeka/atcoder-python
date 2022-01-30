import datetime
import typing

import bs4
import pandas as pd

from atcoder.core.scrape.contest import scrape_contest
from atcoder.core.scrape.utils import _strip_unit, parse_html
from atcoder.core.submission import (
    Submission,
    SubmissionStatus,
    status_from_str,
)
from atcoder.core.utils import unwrap


async def scrape_pagination(
    html: bytes,
) -> typing.Optional[typing.Tuple[int, int]]:
    soup = await parse_html(html)
    pagination = soup.find(class_="pagination")
    if pagination is None:
        return None
    current_page = int(pagination.find(class_="active").text)
    last_page = int(pagination.find_all("li")[-1].text)
    return current_page, last_page


async def scrape_submissions(
    html: bytes,
) -> typing.Optional[typing.List[Submission]]:
    soup = await parse_html(html)
    table = soup.table
    if table is None:
        return None
    contest = await scrape_contest(html)

    async def scrape_submission(row: bs4.element.Tag) -> Submission:
        infos = row.find_all("td")
        if row.find(class_="waiting-judge") is not None:
            status = SubmissionStatus.WJ
        else:
            status = unwrap(status_from_str(infos[6].text.split()[-1]))

        submission = Submission(
            id=infos[-1].a.get("href").split("/")[-1],
            contest_id=contest.id,
            submission_datetime=datetime.datetime.strptime(
                infos[0].time.text,
                "%Y-%m-%d %H:%M:%S%z",
            ),
            task_id=infos[1].a.get("href").split("/")[-1],
            user=infos[2].a.get("href").split("/")[-1],
            language=infos[3].text,
            score=int(infos[4].text),
            code_size_kb=_strip_unit(infos[5].text),
            status=status,
        )
        if submission.status == SubmissionStatus.WJ:
            return submission
        if submission.status != SubmissionStatus.CE:
            submission.exec_time_ms = _strip_unit(infos[7].text)
            submission.memory_usage_kb = _strip_unit(infos[8].text)
        return submission

    return [await scrape_submission(row) for row in table.tbody.find_all("tr")]


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
