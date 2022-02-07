import dataclasses
import json
import os
import typing

import requests


@dataclasses.dataclass(frozen=True)
class LoginCredentials:
    username: str
    password: str


def _input_login_credentials() -> LoginCredentials:
    import getpass

    return LoginCredentials(
        username=input("username: "),
        password=getpass.getpass("password: "),
    )


def _credentials_from_json_file(json_filepath: str) -> LoginCredentials:
    assert os.path.exists(json_filepath)
    with open(file=json_filepath, mode="r", encoding="utf-8") as f:
        credentials_dict: typing.Dict[str, str] = json.load(f)
    return LoginCredentials(**credentials_dict)


def _credentials_from_yaml_file(yaml_filepath: str) -> LoginCredentials:
    ...


def _is_logged_in(session: requests.Session) -> bool:
    import atcoder.contest

    response = session.get(
        url=f"{atcoder.contest._CONTESTS_URL}/abc001/submit",
        allow_redirects=False,
    )
    return response.status_code == 200


class InvalidSessionError(Exception):
    DEFAULT_MESSAGE = "Your login session is invalid. please relogin."

    def __init__(self, message: typing.Optional[str] = None) -> None:
        super().__init__(self.DEFAULT_MESSAGE if message is None else message)
