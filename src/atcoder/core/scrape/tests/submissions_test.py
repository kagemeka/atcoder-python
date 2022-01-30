import asyncio
import unittest
import pprint
from atcoder.core.crawl.submissions import crawl_submissions_page
from atcoder.core.scrape.submissions import (
    scrape_pagination,
    scrape_submissions,
)


class Test(unittest.TestCase):
    def test(self) -> None:
        async def wrap() -> None:
            response = await crawl_submissions_page("abc236", page_id=2)
            print(await scrape_pagination(response.content))
            pprint.pprint(await scrape_submissions(response.content))
            response = await crawl_submissions_page("abc236", page_id=100000)
            pprint.pprint(await scrape_submissions(response.content))

        asyncio.run(wrap())


if __name__ == "__main__":
    unittest.main()
