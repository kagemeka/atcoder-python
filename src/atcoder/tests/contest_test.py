import asyncio
import pprint
import unittest

from atcoder.contest import fetch_all_contests


class Test(unittest.TestCase):
    def test_fetch_contests(self) -> None:
        async def wrap() -> None:
            async for contests in fetch_all_contests():
                pprint.pprint(contests)

        asyncio.run(wrap())


if __name__ == "__main__":
    unittest.main()
