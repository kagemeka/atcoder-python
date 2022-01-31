import dataclasses


@dataclasses.dataclass(frozen=True)
class Auth:
    username: str
    password: str
