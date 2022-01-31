import asyncio
import unittest

import tqdm

from atcoder.core.crawl.submission_results import get_submissions_page
from atcoder.core.scrape.submission_results import (
    scrape_language_categories,
    scrape_pagination,
    scrape_submission_statuses,
    scrape_submissions,
    scrape_task_ids,
)


class Test(unittest.TestCase):
    def test(self) -> None:
        async def wrap() -> None:
            for i in tqdm.trange(1):
                response = await get_submissions_page("abc236", page_id=i + 1)
                await scrape_pagination(response.content)
                await scrape_submissions(response.content)

            response = await get_submissions_page("abc236", page_id=100000)
            self.assertIsNone(await scrape_submissions(response.content))

            response = await get_submissions_page("abc236")
            print(await scrape_language_categories(response.content))
            print(await scrape_submission_statuses(response.content))
            print(await scrape_task_ids(response.content))

        asyncio.run(wrap())


if __name__ == "__main__":
    unittest.main()
