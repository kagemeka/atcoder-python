import asyncio
import os
import unittest

import pytest

import atcoder.auth
import atcoder.login
import atcoder.network


class Test(unittest.TestCase):
    @pytest.mark.skip(reason="auth input needed")
    def test(self) -> None:
        async def wrap() -> None:
            cookies_path = "/tmp/cookies.json"
            credentials = atcoder.auth._input_login_credentials()
            session = atcoder.login.login(credentials)
            self.assertTrue(atcoder.auth._is_logged_in(session))
            atcoder.network._save_cookies(session.cookies, cookies_path)
            del session

            session = atcoder.network._restore_session(cookies_path)
            self.assertTrue(atcoder.auth._is_logged_in(session))
            os.remove(cookies_path)

        asyncio.run(wrap())


if __name__ == "__main__":
    unittest.main()
