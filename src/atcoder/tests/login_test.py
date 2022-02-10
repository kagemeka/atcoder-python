import logging
import unittest

import pytest

import atcoder.auth
import atcoder.login

_LOGGING_FORMAT = "%(asctime)s %(levelname)s %(pathname)s %(message)s"
logging.basicConfig(
    format=_LOGGING_FORMAT,
    datefmt="%Y-%m-%d %H:%M:%S%z",
    handlers=[logging.StreamHandler()],
    level=logging.DEBUG,
)


@pytest.mark.skip(reason="auth input needed")
class Test(unittest.TestCase):
    def test(self) -> None:
        credentials = atcoder.auth._input_login_credentials()
        session = atcoder.login.login(credentials)
        self.assertTrue(atcoder.auth._is_logged_in(session))
        session.close()


if __name__ == "__main__":
    unittest.main()
