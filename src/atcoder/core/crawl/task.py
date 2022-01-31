import requests

from atcoder.core.crawl.constant import CONTESTS_URL


async def get_task_page(
    contest_id: str,
    task_id: str,
) -> requests.models.Response:
    url = f"{CONTESTS_URL}/{contest_id}/tasks/{task_id}"
    return requests.get(url)
