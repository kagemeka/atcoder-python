import asyncio
import unittest

import pytest

from atcoder.core._test_utils import (
    ABC001_1_CODE_PYTHON,
    _login_with_new_session,
)
from atcoder.submit import fetch_languages, submit_task


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
