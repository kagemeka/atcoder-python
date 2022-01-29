from atcoder.crawl.constant import CONTESTS_URL

import requests


async def crawl_submission(
    contest_id: str,
    submission_id: int,
) -> requests.models.Response:
    url = f"{CONTESTS_URL}/{contest_id}/submissions/{submission_id}"
    return requests.get(url)
