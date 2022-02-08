import asyncio
import logging
import unittest

import aiohttp

import atcoder.submission
from atcoder.submission import fetch_all_submission_results

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
            contest_id = "abc001"
            async with aiohttp.ClientSession() as session:
                async for submission in fetch_all_submission_results(
                    session,
                    contest_id,
                    params=atcoder.submission.SubmissionsSearchParams(
                        username="kagemeka"
                    ),
                ):
                    ...

        asyncio.run(wrap())


if __name__ == "__main__":
    unittest.main()
