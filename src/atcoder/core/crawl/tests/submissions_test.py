import asyncio
import unittest

import pytest

from atcoder.core.crawl.submissions import (
    RequestParams,
    crawl_submissions_page,
)


class Test(unittest.TestCase):
    def test(self) -> None:
        async def wrap() -> None:
            params = RequestParams(user="Kagemeka")
            response = await crawl_submissions_page(
                "abc236",
                params,
                page_id=0,
            )
            self.assertEqual(response.status_code, 200)

        asyncio.run(wrap())


if __name__ == "__main__":
    unittest.main()
