from atcoder.scrape.utils import parse_html
from atcoder.utils import unwrap
from atcoder.submission import (
    status_from_str,
    SubmissionSummary,
    JudgeResult,
)
import typing
import pandas as pd


async def scrape_submission_id(html: bytes) -> int:
    import re

    soup = await parse_html(html)
    match = re.match(r"^.*\#(\d+).*$", soup.find(class_="h2").text)
    return unwrap(match).group(1)


def _strip_unit(measured_value: str) -> int:
    # strip unit like "ms" or "kB"
    return int(measured_value.split()[0])


async def scrape_submission_summary(html: bytes) -> SubmissionSummary:
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


async def scrape_code(html: bytes) -> str:
    soup = await parse_html(html)
    return soup.find(id="submission-code").text


async def scrape_judge_details(html: bytes) -> typing.List[JudgeResult]:
    soup = await parse_html(html)
    table = pd.read_html(soup.prettify())[-1]
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
    from atcoder.crawl.submission import crawl_submission
    import asyncio
    import pprint

    async def test() -> None:
        response = await crawl_submission("abc236", 28755333)
        print(await scrape_submission_id(response.content))
        pprint.pprint(await scrape_judge_details(response.content))
        await scrape_submission_summary(response.content)

    asyncio.run(test())
