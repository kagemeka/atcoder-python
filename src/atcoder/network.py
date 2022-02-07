import json
import typing

import requests
import requests.cookies


def _cookies_to_dict(
    cookiejar: requests.cookies.RequestsCookieJar,
) -> typing.Dict[str, typing.Optional[str]]:
    import http.cookiejar

    cookies: typing.List[http.cookiejar.Cookie] = list(cookiejar)
    return {cookie.name: cookie.value for cookie in cookies}


def _restore_session(json_filepath: str) -> requests.Session:
    session = requests.Session()
    session.cookies = _load_cookies(json_filepath)
    return session


def _save_cookies(
    cookies: requests.cookies.RequestsCookieJar,
    json_filepath: str,
) -> None:
    import atcoder.utils

    atcoder.utils._prepare_directory(json_filepath)
    with open(file=json_filepath, mode="w") as f:
        json.dump(_cookies_to_dict(cookies), f)


def _load_cookies(
    json_filepath: str,
) -> requests.cookies.RequestsCookieJar:
    import os

    assert os.path.exists(json_filepath)
    with open(file=json_filepath, mode="r") as f:
        cookies_dict: typing.Dict[str, typing.Optional[str]] = json.load(f)
    return typing.cast(
        requests.cookies.RequestsCookieJar,
        requests.cookies.cookiejar_from_dict(cookies_dict),
    )
