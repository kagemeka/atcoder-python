import asyncio
import logging
import unittest

import aiohttp

import atcoder.contest

_LOGGING_FORMAT = "%(asctime)s %(levelname)s %(pathname)s %(message)s"
logging.basicConfig(
    format=_LOGGING_FORMAT,
    datefmt="%Y-%m-%d %H:%M:%S%z",
    handlers=[logging.StreamHandler()],
    level=logging.DEBUG,
)


class Test(unittest.TestCase):
    def test(self) -> None:
        async def wrap() -> None:
            async with aiohttp.ClientSession() as session:
                contests = []
                async for contest in atcoder.contest.fetch_all_contests(
                    session,
                ):
                    contests.append(contest)
                print(len(contests))
                self.assertTrue(len(contests) >= 880)  # 2022-02-20

        asyncio.run(wrap())


if __name__ == "__main__":
    unittest.main()
