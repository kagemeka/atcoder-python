import dataclasses

import requests

from atcoder.core.crawl.constant import CONTESTS_URL


@dataclasses.dataclass(frozen=True)
class PostData:
    task_id: str
    language_id: int
    source_code: str
    csrf_token: str


async def post_submission(
    contest_id: str,
    post_data: PostData,
    session: requests.Session,
) -> requests.models.Response:
    return session.post(
        f"{CONTESTS_URL}/{contest_id}/submit",
        data={
            "data.TaskScreenName": post_data.task_id,
            "data.LanguageId": post_data.language_id,
            "sourceCode": post_data.source_code,
            "csrf_token": post_data.csrf_token,
        },
    )
