import typing
import dataclasses


@dataclasses.dataclass(frozen=True)
class _LoginCredentials:
    username: str
    password: str


if __name__ == "__main__":
    import asyncio

    async def test() -> None:
        ...

    asyncio.run(test())
