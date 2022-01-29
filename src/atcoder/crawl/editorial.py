import requests

from atcoder.crawl.constant import CONTESTS_URL


async def crawl_editorial(
    contest_id: str,
) -> requests.models.Response:
    url = f"{CONTESTS_URL}/{contest_id}/editorial"
    return requests.get(url)
