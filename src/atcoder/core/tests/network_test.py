import asyncio
import unittest

import pytest
import requests

from atcoder.core._test_utils import _login_with_new_session
from atcoder.core.auth import is_logged_in
from atcoder.core.network import restore_session, save_cookies


class Test(unittest.TestCase):
    @pytest.mark.skip
    def test(self) -> None:
        async def wrap() -> None:
            session = await _login_with_new_session()
            await save_cookies(session.cookies, "/tmp/cookies.json")
            session.close()

            session = requests.Session()
            self.assertFalse(is_logged_in(session))
            session.close()

            session = await restore_session("/tmp/cookies.json")
            self.assertTrue(is_logged_in(session))
            session.close()

        asyncio.run(wrap())


if __name__ == "__main__":
    unittest.main()
