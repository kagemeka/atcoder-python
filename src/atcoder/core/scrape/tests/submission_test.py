import asyncio
import pprint
import unittest

from atcoder.core.crawl.submission_result import get_submission_page
from atcoder.core.scrape.submission_result import scrape_submission_result


class Test(unittest.TestCase):
    def test(self) -> None:
        async def wrap() -> None:
            response = await get_submission_page("abc236", 28755333)
            print(await scrape_submission_result(response.content))

        asyncio.run(wrap())


if __name__ == "__main__":
    unittest.main()
