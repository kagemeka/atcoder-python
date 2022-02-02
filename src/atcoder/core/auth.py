import dataclasses
import json
import os
import typing

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


def credentials_from_json_file(json_filepath: str) -> LoginCredentials:
    assert os.path.exists(json_filepath)
    with open(file=json_filepath, mode="r") as f:
        credentials_dict: typing.Dict[str, str] = json.load(f)
    return LoginCredentials(**credentials_dict)


def credentials_from_yaml_file(yaml_filepath: str) -> LoginCredentials:
    ...


def is_logged_in(session: requests.Session) -> bool:
    from atcoder.core.crawl.constant import CONTESTS_URL

    response = session.get(
        url=f"{CONTESTS_URL}/abc001/submit",
        allow_redirects=False,
    )
    return response.status_code == 200


class InvalidSessionError(Exception):
    DEFAULT_MESSAGE = "Your login session is invalid. please relogin."

    def __init__(self, message: typing.Optional[str] = None) -> None:
        super().__init__(self.DEFAULT_MESSAGE if message is None else message)
