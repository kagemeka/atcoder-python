import asyncio
import unittest

from atcoder.core.crawl.contest import crawl_contest
from atcoder.core.scrape.contest import scrape_contest


class Test(unittest.TestCase):
    def test(self) -> None:
        async def wrap() -> None:
            response = await crawl_contest("abc236")
            print(await scrape_contest(response.content))

        asyncio.run(wrap())


if __name__ == "__main__":
    unittest.main()
