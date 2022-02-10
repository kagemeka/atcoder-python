import unittest

import pytest

import atcoder.auth
import atcoder.login
import atcoder.submit

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


@pytest.mark.skip(reason="auth input needed")
class Test(unittest.TestCase):
    def test_submit(self) -> None:
        credentials = atcoder.auth._input_login_credentials()
        session = atcoder.login.login(credentials)
        atcoder.submit.submit_task(
            session,
            "abc001",
            "abc001_1",
            ABC001_1_CODE_PYTHON,
            4006,  # python3
        )
        session.close()

    def test_fetch_language(self) -> None:

        credentials = atcoder.auth._input_login_credentials()
        session = atcoder.login.login(credentials)
        print(atcoder.submit.fetch_languages(session))
        session.close()


if __name__ == "__main__":
    unittest.main()
