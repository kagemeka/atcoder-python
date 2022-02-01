import dataclasses


@dataclasses.dataclass(frozen=True)
class LoginCredentials:
    username: str
    password: str


def input_login_credentials() -> LoginCredentials:
    return LoginCredentials(
        username=input("username: "),
        password=input("password: "),
    )


import http.client

print(http.client.responses.get(200))
