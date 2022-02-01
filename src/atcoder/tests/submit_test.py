import asyncio
import pprint
import unittest

import pytest

from atcoder.core._test_utils import (
    _login_with_new_session,
    ABC001_1_CODE_PYTHON,
)

from atcoder.submit import submit_task, fetch_languages


@pytest.mark.skip
class Test(unittest.TestCase):
    def test_fetch_languages(self) -> None:
        async def wrap() -> None:
            session = await _login_with_new_session()
            languages = await fetch_languages(session)
            print(languages)

        asyncio.run(wrap())

    def test_submit(self) -> None:
        async def wrap() -> None:
            session = await _login_with_new_session()
            await submit_task(
                session,
                "abc001",
                "abc001_1",
                ABC001_1_CODE_PYTHON,
                4006,
            )

        asyncio.run(wrap())


if __name__ == "__main__":
    unittest.main()
