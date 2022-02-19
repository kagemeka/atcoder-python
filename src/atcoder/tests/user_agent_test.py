import asyncio
import unittest

import pytest

import atcoder.auth
import atcoder.user_agent


class Test(unittest.TestCase):
    @pytest.mark.skip(reason="auth input needed")
    def test(self) -> None:
        async def wrap() -> None:
            with atcoder.user_agent.UserSessionAgent(
                credentials=atcoder.auth._input_login_credentials(),
            ) as user:
                print(user.fetch_languages())
                cnt = 0
                for submission in user.fetch_my_submissions("abc001"):
                    print(submission)
                    ...
                    cnt += 1
                print(cnt)

        asyncio.run(wrap())


if __name__ == "__main__":
    unittest.main()
