import typing

from atcoder.core.contest import Contest


async def fetch_all_contests() -> typing.AsyncIterator[typing.List[Contest]]:
    ...


async def register() -> None:
    ...
