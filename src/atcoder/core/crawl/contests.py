import requests

from atcoder.core.crawl.constant import CONTESTS_URL


async def get_contests_page() -> requests.models.Response:
    return requests.get(CONTESTS_URL, params={"lang": "ja"})
