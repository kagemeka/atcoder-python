import asyncio
import unittest

import pytest

from atcoder.core.auth import input_login_credentials
from atcoder.user_agent import UserSessionAgent


class Test(unittest.TestCase):
    @pytest.mark.skip
    def test(self) -> None:
        async def wrap() -> None:
            with UserSessionAgent(
                credentials=input_login_credentials(),
            ) as user:
                print(await user.fetch_languages())
                async for submissions in user.fetch_my_submissions("abc001"):
                    print(submissions)

        asyncio.run(wrap())


if __name__ == "__main__":
    unittest.main()
