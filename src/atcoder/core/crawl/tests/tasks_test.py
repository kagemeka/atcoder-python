import asyncio
import unittest

from atcoder.core.crawl.tasks import get_tasks_page


class Test(unittest.TestCase):
    def test(self) -> None:
        async def wrap() -> None:
            response = await get_tasks_page(contest_id="abc236")
            self.assertEqual(response.status_code, 200)

        asyncio.run(wrap())


if __name__ == "__main__":
    unittest.main()
