import asyncio
import unittest

from atcoder.core.crawl.contests import get_contests_page


class Test(unittest.TestCase):
    def test(self) -> None:
        async def wrap() -> None:
            response = await get_contests_page()
            self.assertEqual(response.status_code, 200)

        asyncio.run(wrap())


if __name__ == "__main__":
    unittest.main()
