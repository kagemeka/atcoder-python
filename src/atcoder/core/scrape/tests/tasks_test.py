import asyncio
import pprint
import unittest

from atcoder.core.crawl.tasks import crawl_tasks
from atcoder.core.scrape.tasks import scrape_tasks


class Test(unittest.TestCase):
    def test(self) -> None:
        async def wrap() -> None:
            response = await crawl_tasks("abc236")
            pprint.pprint(await scrape_tasks(response.content))

        asyncio.run(wrap())


if __name__ == "__main__":
    unittest.main()
