import dataclasses

import requests

from atcoder.core.crawl.constant import CONTESTS_URL


def make_submit_url(contest_id: str) -> str:
    return f"{CONTESTS_URL}/{contest_id}/submit"


async def get_submit_page(
    session: requests.Session,
    contest_id: str,
) -> requests.models.Response:
    return session.get(make_submit_url(contest_id))


@dataclasses.dataclass(frozen=True)
class SubmitPostParams:
    task_id: str
    language_id: int
    source_code: str
    csrf_token: str


async def post_submission(
    session: requests.Session,
    contest_id: str,
    post_params: SubmitPostParams,
) -> requests.models.Response:
    return session.post(
        url=make_submit_url(contest_id),
        data={
            "data.TaskScreenName": post_params.task_id,
            "data.LanguageId": post_params.language_id,
            "sourceCode": post_params.source_code,
            "csrf_token": post_params.csrf_token,
        },
    )
