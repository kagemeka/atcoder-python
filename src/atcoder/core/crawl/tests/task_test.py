import asyncio
import unittest

from atcoder.core.crawl.task import get_task_page


class Test(unittest.TestCase):
    def test(self) -> None:
        async def wrap() -> None:
            response = await get_task_page(
                contest_id="abc236",
                task_id="abc236_a",
            )
            self.assertEqual(response.status_code, 200)

        asyncio.run(wrap())


if __name__ == "__main__":
    unittest.main()
