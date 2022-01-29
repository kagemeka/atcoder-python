from atcoder.scrape.utils import parse_html
from atcoder.utils import unwrap



async def scrape_contest_id(html: bytes) -> int:
    import re

    soup = await parse_html(html)
    match = re.match(r"^.*\#(\d+).*$", soup.find(class_="h2").text)
    return unwrap(match).group(1)


async def scrape_code(html: bytes) -> str:
    soup = await parse_html(html)
    return soup.find(id="submission-code").text


if __name__ == "__main__":
    from atcoder.crawl.submission import crawl_submission
    import asyncio

    async def test() -> None:
        response = await crawl_submission("abc236")
        print(await scrape_submission_id(response.content))

    asyncio.run(test())
