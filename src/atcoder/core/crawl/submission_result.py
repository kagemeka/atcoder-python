import requests

from atcoder.core.crawl.constant import CONTESTS_URL


async def get_submission_page(
    contest_id: str,
    submission_id: int,
) -> requests.models.Response:
    url = f"{CONTESTS_URL}/{contest_id}/submissions/{submission_id}"
    return requests.get(url)
