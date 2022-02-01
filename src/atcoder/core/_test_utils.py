import dataclasses
import http.client
import logging

import requests

from atcoder.core.auth import input_login_credentials
from atcoder.core.crawl.login import (
    LoginPostParams,
    get_login_page,
    post_login,
)
from atcoder.core.scrape.login import scrape_csrf_token

logger = logging.getLogger(__name__)


async def _login_with_new_session() -> requests.Session:
    session = requests.session()
    response = await get_login_page(session)
    token = await scrape_csrf_token(response.content)
    credentials = input_login_credentials()
    response = await post_login(
        session,
        LoginPostParams(
            **dataclasses.asdict(credentials),
            csrf_token=token,
        ),
    )
    logger.debug(
        f"{response.status_code}"
        f" {http.client.responses.get(response.status_code)}"
    )

    return session


ABC001_1_CODE_PYTHON = """
# API Code Submission Test.
import typing

def main() -> None:
    h1 = int(input())
    h2 = int(input())
    print(h1 - h2)

if __name__ == '__main__':
    main()
"""
