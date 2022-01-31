import typing

import pandas as pd

from atcoder.core.scrape.utils import _strip_unit, parse_html
from atcoder.core.submission_result import (
    JudgeResult,
    SubmissionDetails,
    SubmissionResult,
    SubmissionStatus,
    SubmissionSummary,
    status_from_str,
)
from atcoder.core.utils import unwrap


async def scrape_id(html: bytes) -> int:
    import re

    soup = await parse_html(html)
    match = re.match(r"^.*\#(\d+).*$", soup.find(class_="h2").text)
    return int(unwrap(match).group(1))


async def scrape_summary(html: bytes) -> SubmissionSummary:
    import datetime

    soup = await parse_html(html)
    infos = soup.table.find_all("tr")
    assert len(infos) >= 8
    if soup.table.find(class_="waiting-judge") is not None:
        status = SubmissionStatus.WJ
    else:
        status = unwrap(status_from_str(infos[6].td.text.split()[-1]))
    if len(infos) == 9:
        exec_time_ms = _strip_unit(infos[7].td.text)
        memory_usage_kb = _strip_unit(infos[8].td.text)
    else:
        exec_time_ms = None
        memory_usage_kb = None
    return SubmissionSummary(
        datetime=datetime.datetime.strptime(
            infos[0].time.text,
            "%Y-%m-%d %H:%M:%S%z",
        ),
        task_id=infos[1].a.get("href").split("/")[-1],
        user_id=infos[2].a.get("href").split("/")[-1],
        language_id=infos[3].td.text,
        score=int(infos[4].td.text),
        code_size_kb=_strip_unit(infos[5].td.text),
        status=status,
        exec_time_ms=exec_time_ms,
        memory_usage_kb=memory_usage_kb,
    )


async def scrape_submission_result(html: bytes) -> SubmissionResult:
    return SubmissionResult(
        id=await scrape_id(html),
        summary=await scrape_summary(html),
        details=await scrape_details(html),
    )


async def scrape_code(html: bytes) -> str:
    soup = await parse_html(html)
    return typing.cast(str, soup.find(id="submission-code").text)


async def scrape_judge_results(html: bytes) -> typing.List[JudgeResult]:
    table = pd.read_html(html)[-1]
    table.rename(
        columns={
            "Case Name": "case_name",
            "Status": "status",
            "Exec Time": "exec_time_ms",
            "Memory": "memory_usage_kb",
        },
        inplace=True,
    )
    table["exec_time_ms"] = table["exec_time_ms"].map(_strip_unit)
    table["memory_usage_kb"] = table["memory_usage_kb"].map(_strip_unit)
    table["status"] = table["status"].map(status_from_str)
    records = table.to_dict(orient="records")
    return [JudgeResult(**record) for record in records]


async def scrape_details(html: bytes) -> SubmissionDetails:
    return SubmissionDetails(
        code=await scrape_code(html),
        judge_results=await scrape_judge_results(html),
    )


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
