import asyncio
import pprint
import unittest

from atcoder.core.crawl.submissions import crawl_submissions_page
from atcoder.core.scrape.submissions import (
    scrape_pagination,
    scrape_submissions,
)


class Test(unittest.TestCase):
    def test(self) -> None:
        async def wrap() -> None:
            for i in range(10):
                response = await crawl_submissions_page(
                    "abc236", page_id=i + 1
                )
                print(i)
                await scrape_pagination(response.content)
                pprint.pprint(await scrape_submissions(response.content))
                print(i)
                await asyncio.sleep(1)
            response = await crawl_submissions_page("abc236", page_id=100000)
            self.assertIsNone(await scrape_submissions(response.content))

        asyncio.run(wrap())


if __name__ == "__main__":
    unittest.main()
