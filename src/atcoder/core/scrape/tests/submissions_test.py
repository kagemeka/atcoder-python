import asyncio
import pprint
import unittest

import tqdm

from atcoder.core.crawl.submissions import crawl_submissions_page
from atcoder.core.scrape.submissions import (
    scrape_pagination,
    scrape_submissions,
)


class Test(unittest.TestCase):
    def test(self) -> None:
        async def wrap() -> None:
            for i in tqdm.trange(1):
                response = await crawl_submissions_page(
                    "abc236", page_id=i + 1
                )
                await scrape_pagination(response.content)
                await scrape_submissions(response.content)

            response = await crawl_submissions_page("abc236", page_id=100000)
            self.assertIsNone(await scrape_submissions(response.content))

        asyncio.run(wrap())


if __name__ == "__main__":
    unittest.main()
