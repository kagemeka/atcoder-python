import dataclasses
import datetime
import typing

from atcoder.submission_status import SubmissionStatus, status_from_str
from atcoder.utils import unwrap


@dataclasses.dataclass
class SubmissionInfo:
    submission_time: datetime.datetime
    task_id: str
    user: str
    language: int
    score: int
    code_size: int
    status: SubmissionStatus
    exec_time: int  # ms
    memory: int  # kB


async def scrape_submission_info(html: bytes) -> SubmissionInfo:
    soup = await parse_html(html)
    infos = soup.table.find_all("tr")
    return SubmissionInfo(
        submission_time=datetime.datetime.strptime(
            infos[0].time.text,
            "%Y-%m-%d %H:%M:%S%z",
        ),
        task_id=infos[1].a.get("href").split("/")[-1],
        user=infos[2].a.get("href").split("/")[-1],
        language=infos[3].td.text,
        score=int(infos[4].td.text),
        code_size=int(infos[5].td.text.split()[0]),
        status=unwrap(status_from_str(infos[6].td.text)),
        exec_time=int(infos[7].td.text.split()[0]),
        memory=int(infos[8].td.text.split()[0]),
    )


async def scrape_code(html: bytes) -> str:
    ...


if __name__ == "__main__":
    from atcoder.crawl.submission import crawl_submission
    from atcoder.scrape.utils import parse_html
    import asyncio

    async def test() -> None:
        response = await crawl_submission("abc236", 28755333)
        submission_info = await scrape_submission_info(response.content)
        print(submission_info)
        # soup = await parse_html(response.content)
        # print(soup.prettify())

    asyncio.run(test())
