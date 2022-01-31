import asyncio
import unittest

from atcoder.core.crawl.contest import get_contest_page
from atcoder.core.scrape.contest import scrape_contest


class Test(unittest.TestCase):
    def test(self) -> None:
        async def wrap() -> None:
            response = await get_contest_page("abc236")
            print(await scrape_contest(response.content))

        asyncio.run(wrap())


if __name__ == "__main__":
    unittest.main()
