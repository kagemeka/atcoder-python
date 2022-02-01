import dataclasses
import http.client
import logging

import requests

from atcoder.core.auth import (
    InvalidSessionError,
    LoginCredentials,
    is_logged_in,
)
from atcoder.core.crawl.login import (
    LoginPostParams,
    get_login_page,
    post_login,
)
from atcoder.core.scrape.login import scrape_csrf_token

logger = logging.getLogger(__name__)


async def login(credentials: LoginCredentials) -> requests.Session:
    session = requests.session()
    response = await get_login_page(session)
    token = await scrape_csrf_token(response.content)
    response = await post_login(
        session,
        LoginPostParams(
            **dataclasses.asdict(credentials),
            csrf_token=token,
        ),
    )
    if not is_logged_in(session):
        raise InvalidSessionError(
            "Cannot login to atcoder.jp, please check your credentials",
        )
    logger.debug(
        f"{response.status_code}"
        f" {http.client.responses.get(response.status_code)}"
    )
    return session
