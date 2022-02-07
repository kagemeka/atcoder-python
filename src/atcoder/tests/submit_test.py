import asyncio
import unittest

import atcoder.auth
import atcoder.login
import atcoder.submit
import pytest

ABC001_1_CODE_PYTHON = """
# API Code Submission Test.
import typing

def main() -> None:
    h1 = int(input())
    h2 = int(input())
    print(h1 - h2)

if __name__ == '__main__':
    main()
"""


@pytest.mark.skip
class Test(unittest.TestCase):
    def test_submit(self) -> None:
        async def wrap() -> None:
            credentials = atcoder.auth._input_login_credentials()
            session = atcoder.login._login(credentials)
            atcoder.submit._submit_task(
                session,
                "abc001",
                "abc001_1",
                ABC001_1_CODE_PYTHON,
                4006,
            )

        asyncio.run(wrap())


if __name__ == "__main__":
    unittest.main()
