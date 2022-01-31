import asyncio
import unittest

from atcoder.core.crawl.contests_archive import get_contests_archive_page


class Test(unittest.TestCase):
    def test(self) -> None:
        async def wrap() -> None:
            response = await get_contests_archive_page()
            self.assertEqual(response.status_code, 200)
            response = await get_contests_archive_page(page_id=1)
            self.assertEqual(response.status_code, 200)
            response = await get_contests_archive_page(page_id=100)
            self.assertEqual(response.status_code, 200)

        asyncio.run(wrap())


if __name__ == "__main__":
    unittest.main()
