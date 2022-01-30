import dataclasses


@dataclasses.dataclass
class Auth:
    username: str
    password: str
