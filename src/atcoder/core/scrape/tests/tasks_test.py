import asyncio
import pprint
import unittest

from atcoder.core.crawl.tasks import get_tasks_page
from atcoder.core.scrape.tasks import scrape_tasks


class Test(unittest.TestCase):
    def test(self) -> None:
        async def wrap() -> None:
            response = await get_tasks_page("abc236")
            pprint.pprint(await scrape_tasks(response.content))

        asyncio.run(wrap())


if __name__ == "__main__":
    unittest.main()
