import typing

import requests

from atcoder.core.crawl.constant import CONTESTS_URL


async def get_contests_archive_page(
    page_id: typing.Optional[int] = None,
) -> requests.models.Response:
    return requests.get(
        url=f"{CONTESTS_URL}/archive",
        params={
            "page": page_id,
            "lang": "ja",
        },
    )
