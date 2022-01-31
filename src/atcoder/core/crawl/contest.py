import requests

from atcoder.core.crawl.constant import CONTESTS_URL


async def get_contest_page(
    contest_id: str,
) -> requests.models.Response:
    url = f"{CONTESTS_URL}/{contest_id}"
    return requests.get(url)
