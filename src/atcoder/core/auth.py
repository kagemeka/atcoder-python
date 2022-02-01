import dataclasses

import requests


@dataclasses.dataclass(frozen=True)
class LoginCredentials:
    username: str
    password: str


def input_login_credentials() -> LoginCredentials:
    return LoginCredentials(
        username=input("username: "),
        password=input("password: "),
    )


def is_logged_in(session: requests.Session) -> bool:
    from atcoder.core.crawl.constant import CONTESTS_URL

    response = session.get(
        url=f"{CONTESTS_URL}/abc001/submit",
        allow_redirects=False,
    )
    return response.status_code == 200
