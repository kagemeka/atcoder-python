import asyncio
import unittest

import bs4
import pytest

from atcoder.core._test_utils import _login_with_new_session
from atcoder.core.crawl.constant import CONTESTS_URL


class Test(unittest.TestCase):
    @pytest.mark.skip
    def test_post_login(self) -> None:
        async def wrap() -> None:
            session = await _login_with_new_session()
            response = session.get(f"{CONTESTS_URL}/abc236/submissions/me")
            print(response.status_code)
            soup = bs4.BeautifulSoup(response.content, "html.parser")
            print(soup.prettify())
            print(type(session.cookies))

        asyncio.run(wrap())


if __name__ == "__main__":
    unittest.main()
