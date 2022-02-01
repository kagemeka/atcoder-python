import asyncio
import pprint
import unittest

import pytest

from atcoder.core._test_utils import _login_with_new_session
from atcoder.core.crawl.submission_results import SubmissionsSearchParams
from atcoder.submission_result import (
    fetch_all_my_submission_results,
    fetch_all_submission_results,
    fetch_submission_details,
    fetch_submission_results_page_count,
)


@pytest.mark.skip
class Test(unittest.TestCase):
    def test_all_my_submission_results(self) -> None:
        async def wrap() -> None:
            session = await _login_with_new_session()
            async for submissions in fetch_all_my_submission_results(
                session,
                "abc001",
            ):
                pprint.pprint(submissions)
            session.close()

        asyncio.run(wrap())

    def test_all_submission_results(self) -> None:
        async def wrap() -> None:
            params = SubmissionsSearchParams(
                username="pseudo_user_abc5647382910"
            )
            async for submissions in fetch_all_submission_results(
                "abc001",
                params,
            ):
                pprint.pprint(submissions)

        asyncio.run(wrap())

    def test_details(self) -> None:
        async def wrap() -> None:
            submission_id = 106887
            contest_id = "abc001"
            submission_result = await fetch_submission_details(
                contest_id,
                submission_id,
            )
            print(submission_result)

        asyncio.run(wrap())

    def test_page_count(self) -> None:
        async def wrap() -> None:
            page_count = await fetch_submission_results_page_count("abc001")
            print(page_count)

        asyncio.run(wrap())


if __name__ == "__main__":
    unittest.main()
