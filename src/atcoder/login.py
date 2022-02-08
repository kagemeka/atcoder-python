import dataclasses
import http
import logging
import typing

import requests

import atcoder.auth
import atcoder.scrape
import atcoder.utils
from atcoder.constant import _SITE_URL

_LOGIN_URL = f"{_SITE_URL}/login"
_LOGGER = logging.getLogger(__name__)


@dataclasses.dataclass
class _LoginPostParams:
    username: str
    password: str
    csrf_token: str


def _get_login_page(
    session: typing.Optional[requests.Session] = None,
) -> requests.Response:
    if session is None:
        return requests.get(_LOGIN_URL)
    return session.get(_LOGIN_URL)


def _scrape_csrf_token(html: str) -> str:
    soup = atcoder.scrape._parse_html(html)
    return atcoder.utils._unwrap(
        atcoder.scrape._scrape_csrf_token_in_form(soup.find_all("form")[1])
    )


def _post_login_info(
    session: requests.Session,
    params: _LoginPostParams,
) -> requests.Response:
    return session.post(
        url=_LOGIN_URL,
        data=dataclasses.asdict(params),
    )


def login(
    credentials: atcoder.auth.LoginCredentials,
) -> requests.Session:
    session = requests.session()
    response = _get_login_page(session)
    token = _scrape_csrf_token(response.text)
    response = _post_login_info(
        session,
        _LoginPostParams(
            **dataclasses.asdict(credentials),
            csrf_token=token,
        ),
    )
    if not atcoder.auth._is_logged_in(session):
        raise atcoder.auth.InvalidSessionError(
            "Cannot login to atcoder.jp, please check your credentials.",
        )
    _LOGGER.info(
        f"login to atcoder: {http.client.responses.get(response.status_code)}"
    )
    return session
