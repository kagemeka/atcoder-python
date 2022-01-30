import asyncio
import pprint
import unittest

from atcoder.core.crawl.submission import crawl_submission
from atcoder.core.scrape.submission import (
    scrape_code,
    scrape_id,
    scrape_judge_details,
    scrape_summary,
)


class Test(unittest.TestCase):
    def test(self) -> None:
        async def wrap() -> None:
            response = await crawl_submission("abc236", 28755333)
            print(await scrape_id(response.content))
            print(await scrape_summary(response.content))
            print(await scrape_code(response.content))
            pprint.pprint(await scrape_judge_details(response.content))

        asyncio.run(wrap())


if __name__ == "__main__":
    unittest.main()
