import dataclasses
import typing

import requests

from atcoder.core.crawl.constant import LOGIN_URL


async def get_login_page(
    session: typing.Optional[requests.Session] = None,
) -> requests.models.Response:
    if session is None:
        return requests.get(LOGIN_URL)
    return session.get(LOGIN_URL)


@dataclasses.dataclass
class LoginPostParams:
    username: str
    password: str
    csrf_token: str


async def post_login(
    session: requests.Session,
    post_params: LoginPostParams,
) -> requests.models.Response:
    return session.post(
        url=LOGIN_URL,
        data=dataclasses.asdict(post_params),
    )
