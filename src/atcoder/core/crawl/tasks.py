import requests

from atcoder.core.crawl.constant import CONTESTS_URL


async def crawl_tasks(
    contest_id: str,
) -> requests.models.Response:
    url = f"{CONTESTS_URL}/{contest_id}/tasks"
    return requests.get(url)
