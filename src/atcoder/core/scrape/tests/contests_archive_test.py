import asyncio
import pprint
import unittest

from atcoder.core.crawl.contests_archive import get_contests_archive_page
from atcoder.core.scrape.contests_archive import (
    scrape_finished_contests,
    scrape_pagination,
)


class Test(unittest.TestCase):
    def test(self) -> None:
        async def wrap() -> None:

            response = await get_contests_archive_page()
            contests = await scrape_finished_contests(response.content)
            pprint.pprint(contests)

            print(await scrape_pagination(response.content))

        asyncio.run(wrap())


if __name__ == "__main__":
    unittest.main()
