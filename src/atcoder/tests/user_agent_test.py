import asyncio
import unittest

import atcoder.auth
import atcoder.user_agent
import pytest


class Test(unittest.TestCase):
    @pytest.mark.skip
    def test(self) -> None:
        async def wrap() -> None:
            with atcoder.user_agent.UserSessionAgent(
                credentials=atcoder.auth._input_login_credentials(),
            ) as user:
                print(user.fetch_languages())
                for submissions in user.fetch_my_submissions("abc001"):
                    print(submissions)

        asyncio.run(wrap())


if __name__ == "__main__":
    unittest.main()
