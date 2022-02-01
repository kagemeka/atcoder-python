import asyncio
import pprint
import unittest

import pytest

from atcoder.core._test_utils import _login_with_new_session
from atcoder.core.crawl.submit import get_submit_page
from atcoder.core.scrape.submit import (
    scrape_csrf_token,
    scrape_languages,
    scrape_task_ids,
)


class Test(unittest.TestCase):
    @pytest.mark.skip
    def test(self) -> None:
        async def wrap() -> None:
            session = await _login_with_new_session()
            response = await get_submit_page(session, "abc236")
            print(await scrape_csrf_token(response.content))
            await scrape_task_ids(response.content)
            pprint.pprint(await scrape_languages(response.content))

        asyncio.run(wrap())


if __name__ == "__main__":
    unittest.main()
