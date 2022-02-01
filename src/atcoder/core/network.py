import http.cookiejar
import json
import os
import typing

import requests
import requests.cookies


async def _cookies_to_dict(
    cookiejar: requests.cookies.RequestsCookieJar,
) -> typing.Dict[str, typing.Optional[str]]:
    cookies: typing.List[http.cookiejar.Cookie] = list(cookiejar)
    return {cookie.name: cookie.value for cookie in cookies}


async def restore_session(json_filepath: str) -> requests.Session:
    session = requests.Session()
    session.cookies = await load_cookies(json_filepath)
    return session


async def save_cookies(
    cookies: requests.cookies.RequestsCookieJar,
    json_filepath: str,
) -> None:
    os.makedirs(os.path.dirname(json_filepath), exist_ok=True)
    with open(file=json_filepath, mode="w") as f:
        json.dump(await _cookies_to_dict(cookies), f)


async def load_cookies(
    json_filepath: str,
) -> requests.cookies.RequestsCookieJar:
    assert os.path.exists(json_filepath)
    with open(file=json_filepath, mode="r") as f:
        cookies_dict: typing.Dict[str, typing.Optional[str]] = json.load(f)
    return typing.cast(
        requests.cookies.RequestsCookieJar,
        requests.cookies.cookiejar_from_dict(cookies_dict),
    )
