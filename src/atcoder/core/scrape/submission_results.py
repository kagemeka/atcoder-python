import datetime
import typing

import bs4

from atcoder.core.scrape.utils import (
    _scrape_html_options,
    _strip_unit,
    parse_html,
)
from atcoder.core.submission_result import (
    SubmissionResult,
    SubmissionStatus,
    SubmissionSummary,
    status_from_str,
)
from atcoder.core.utils import unwrap


async def scrape_task_ids(html: bytes) -> typing.List[str]:
    return unwrap(await _scrape_html_options(html, "select-task"))


async def scrape_language_categories(html: bytes) -> typing.List[str]:
    return unwrap(await _scrape_html_options(html, "select-language"))


async def scrape_submission_statuses(html: bytes) -> typing.List[str]:
    return unwrap(await _scrape_html_options(html, "select-status"))


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
) -> typing.Optional[typing.List[SubmissionResult]]:
    soup = await parse_html(html)
    table = soup.table
    if table is None:
        return None

    async def scrape_submission(row: bs4.element.Tag) -> SubmissionResult:
        infos = row.find_all("td")
        assert len(infos) >= 8
        if row.find(class_="waiting-judge") is not None:
            status = SubmissionStatus.WJ
        else:
            status = unwrap(status_from_str(infos[6].text.split()[-1]))
        if len(infos) == 10:
            exec_time_ms = _strip_unit(infos[7].text)
            memory_usage_kb = _strip_unit(infos[8].text)
        else:
            exec_time_ms = None
            memory_usage_kb = None
        summary = SubmissionSummary(
            datetime=datetime.datetime.strptime(
                infos[0].time.text,
                "%Y-%m-%d %H:%M:%S%z",
            ),
            task_id=infos[1].a.get("href").split("/")[-1],
            username=infos[2].a.get("href").split("/")[-1],
            language_string=infos[3].text,
            score=int(infos[4].text),
            code_size_kb=_strip_unit(infos[5].text),
            status=status,
            exec_time_ms=exec_time_ms,
            memory_usage_kb=memory_usage_kb,
        )
        return SubmissionResult(
            id=infos[-1].a.get("href").split("/")[-1],
            summary=summary,
        )

    return [await scrape_submission(row) for row in table.tbody.find_all("tr")]


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
