import typing
import datetime
import pandas as pd
import bs4
from atcoder.core.scrape.contest import scrape_contest
from atcoder.core.scrape.utils import _strip_unit, parse_html
from atcoder.core.submission import (
    Submission,
    SubmissionStatus,
    SubmissionSummary,
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


async def _scrape_submission(row: bs4.element.Tag) -> Submission:
    infos = row.find_all("td")
    status = unwrap(status_from_str(infos[6].text))
    summary = SubmissionSummary(
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
    detail_index = 7
    if status != SubmissionStatus.CE:
        summary.exec_time = _strip_unit(infos[7].text)
        summary.memory_usage = _strip_unit(infos[8].text)
        detail_index += 2
    return Submission(
        id=infos[detail_index].a.get("href").split("/")[-1],
        summary=summary,
    )


async def scrape_submissions(
    html: bytes,
) -> typing.Optional[typing.List[Submission]]:
    soup = await parse_html(html)
    table = soup.table
    if table is None:
        return None
    contest = await scrape_contest(html)
    submissions = []
    for row in table.tbody.find_all("tr"):
        submission = await _scrape_submission(row)
        submission.contest_id = contest.id
        submissions.append(submission)
    return submissions


async def scrape_summary(html: bytes) -> SubmissionSummary:
    import datetime

    soup = await parse_html(html)
    infos = soup.table.find_all("tr")
    return SubmissionSummary(
        datetime=datetime.datetime.strptime(
            infos[0].time.text,
            "%Y-%m-%d %H:%M:%S%z",
        ),
        task_id=infos[1].a.get("href").split("/")[-1],
        user=infos[2].a.get("href").split("/")[-1],
        language=infos[3].td.text,
        score=int(infos[4].td.text),
        code_size=_strip_unit(infos[5].td.text),
        status=unwrap(status_from_str(infos[6].td.text)),
        exec_time=_strip_unit(infos[7].td.text),
        memory_usage=_strip_unit(infos[8].td.text),
    )


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
