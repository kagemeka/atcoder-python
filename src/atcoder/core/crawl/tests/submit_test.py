import asyncio
import unittest

import pytest

from atcoder.core._test_utils import (
    _login_with_new_session,
    ABC001_1_CODE_PYTHON,
)
from atcoder.core.crawl.submit import (
    SubmitPostParams,
    get_submit_page,
    post_submission,
)
from atcoder.core.scrape.submit import scrape_csrf_token


class Test(unittest.TestCase):
    @pytest.mark.skip
    def test(self) -> None:
        async def wrap() -> None:
            session = await _login_with_new_session()
            response = await get_submit_page(session, "abc001")
            token = await scrape_csrf_token(response.content)
            params = SubmitPostParams(
                task_id="abc001_1",
                language_id=4006,
                source_code=ABC001_1_CODE_PYTHON,
                csrf_token=token,
            )
            response = await post_submission(session, "abc001", params)
            session.close()

        asyncio.run(wrap())


if __name__ == "__main__":
    unittest.main()
