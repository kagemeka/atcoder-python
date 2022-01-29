import requests

from atcoder.crawl.constant import CONTESTS_URL


async def crawl_task(
    contest_id: str,
    task_id: str,
) -> requests.models.Response:
    url = f"{CONTESTS_URL}/{contest_id}/tasks/{task_id}"
    return requests.get(url)
