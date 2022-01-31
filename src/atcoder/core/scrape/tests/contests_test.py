import asyncio
import pprint
import unittest

from atcoder.core.crawl.contests import get_contests_page
from atcoder.core.scrape.contests import (
    scrape_permanent_contests,
    scrape_running_contests,
    scrape_upcoming_contests,
)


class Test(unittest.TestCase):
    def test(self) -> None:
        async def wrap() -> None:

            response = await get_contests_page()
            contests = await scrape_running_contests(response.content)
            pprint.pprint(contests)

            contests = await scrape_upcoming_contests(response.content)
            pprint.pprint(contests)

            contests = await scrape_permanent_contests(response.content)
            pprint.pprint(contests)

        asyncio.run(wrap())


if __name__ == "__main__":
    unittest.main()
