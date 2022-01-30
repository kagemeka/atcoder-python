import typing

import pandas as pd

from atcoder.core.scrape.utils import _strip_unit, parse_html
from atcoder.core.submission import (
    JudgeResult,
    Submission,
    SubmissionStatus,
    status_from_str,
)
from atcoder.core.utils import unwrap


async def scrape_id(html: bytes) -> int:
    import re

    soup = await parse_html(html)
    match = re.match(r"^.*\#(\d+).*$", soup.find(class_="h2").text)
    return unwrap(match).group(1)


async def scrape_summary(html: bytes) -> Submission:
    import datetime

    soup = await parse_html(html)
    infos = soup.table.find_all("tr")
    submission = Submission(
        id=await scrape_id(html),
        submission_datetime=datetime.datetime.strptime(
            infos[0].time.text,
            "%Y-%m-%d %H:%M:%S%z",
        ),
        task_id=infos[1].a.get("href").split("/")[-1],
        user=infos[2].a.get("href").split("/")[-1],
        language=infos[3].td.text,
        score=int(infos[4].td.text),
        code_size_kb=_strip_unit(infos[5].td.text),
        status=unwrap(status_from_str(infos[6].td.text.split()[-1])),
    )
    if submission.status != SubmissionStatus.CE:
        submission.exec_time_ms = _strip_unit(infos[7].td.text)
        submission.memory_usage_kb = _strip_unit(infos[8].td.text)
    return submission


async def scrape_code(html: bytes) -> str:
    soup = await parse_html(html)
    return soup.find(id="submission-code").text


async def scrape_judge_details(html: bytes) -> typing.List[JudgeResult]:
    table = pd.read_html(html)[-1]
    table.rename(
        columns={
            "Case Name": "case_name",
            "Status": "status",
            "Exec Time": "exec_time",
            "Memory": "memory_usage",
        },
        inplace=True,
    )
    table["exec_time"] = table["exec_time"].map(_strip_unit)
    table["memory_usage"] = table["memory_usage"].map(_strip_unit)
    table["status"] = table["status"].map(status_from_str)
    records = table.to_dict(orient="records")
    return [JudgeResult(**record) for record in records]


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
