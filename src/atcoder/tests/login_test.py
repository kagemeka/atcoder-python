import asyncio
import unittest

import pytest

from atcoder.core.auth import input_login_credentials, is_logged_in
from atcoder.login import login


class Test(unittest.TestCase):
    @pytest.mark.skip
    def test(self) -> None:
        async def wrap() -> None:
            credentials = input_login_credentials()
            session = await login(credentials)
            self.assertTrue(is_logged_in(session))

        asyncio.run(wrap())


if __name__ == "__main__":
    unittest.main()
