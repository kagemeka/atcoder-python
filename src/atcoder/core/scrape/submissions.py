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

    async def scrape_submission(
        row: bs4.element.Tag,
    ) -> typing.Optional[Submission]:
        if row.find(class_="waiting-judge") is not None:
            return None
        infos = row.find_all("td")
        status = unwrap(status_from_str(infos[6].text.split()[-1]))
        detail_index = 7
        if status != SubmissionStatus.CE:
            detail_index += 2
        submission = Submission(
            id=infos[detail_index].a.get("href").split("/")[-1],
            contest_id=contest.id,
            datetime=datetime.datetime.strptime(
                infos[0].time.text,
                "%Y-%m-%d %H:%M:%S%z",
            ),
            task_id=infos[1].a.get("href").split("/")[-1],
            user=infos[2].a.get("href").split("/")[-1],
            language=infos[3].text,
            score=int(infos[4].text),
            code_size=_strip_unit(infos[5].text),
            status=status,
        )
        if status != SubmissionStatus.CE:
            submission.exec_time = _strip_unit(infos[7].text)
            submission.memory_usage = _strip_unit(infos[8].text)
        return submission

    submissions = []
    for row in table.tbody.find_all("tr"):
        submission = await scrape_submission(row)
        if submission is not None:
            submissions.append(submission)
    return submissions


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
