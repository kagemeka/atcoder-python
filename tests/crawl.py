import asyncio
import typing

import bs4
import requests

from atcoder.crawl.submissions import RequestParams, crawl_submissions_page
from atcoder.crawl.utils import fetch_page_source
from atcoder.scrape.utils import parse_html


async def main() -> None:
    params = RequestParams(task_id="abc236_a", user="Kagemeka")
    response = await crawl_submissions_page("abc236", params, page_id=0)
    soup = await parse_html(response.content)
    print(soup.prettify())


if __name__ == "__main__":
    asyncio.run(main())
